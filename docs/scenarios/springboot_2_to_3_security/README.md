# Modernizing a Spring Boot 2 Application to Spring Boot 3 Using Konveyor AI

## Goal

This scenario demonstrates how **Konveyor AI (Kai)** can streamline the migration of a **Spring Boot 2** application to **Spring Boot 3**, **Java 17**, and **Jakarta EE**. We will use a combination of **default** and **custom rules** to:

- Detect deprecated APIs like `WebSecurityConfigurerAdapter`
- Update `javax.*` imports to `jakarta.*`
- Ensure compliance with Java 17

The sample application used is [`springboot_simplelogin`](https://github.com/savitharaghunathan/springboot_simplelogin), and the custom rules are located [here](https://github.com/savitharaghunathan/custom_rules/tree/main/springlogin).

## Background

Spring Boot 3 enforces significant changes including:

- Jakarta EE 9+ migration (`javax.*` -> `jakarta.*`)
- Java 17 as the baseline JDK
- Removal of legacy security configurations

These changes often break compilation and require manual refactoring. With Kai, developers can:

- Automatically identify and resolve breaking changes
- Get LLM-powered refactoring suggestions
- Apply consistent migration patterns across projects using custom rules

## Prerequisites

- [VSCode](https://code.visualstudio.com/download)
- [Git](https://git-scm.com/downloads)
- [GenAI credentials](https://github.com/konveyor/kai/blob/main/docs/llm_selection.md#openai-service)
- Java 17
- Maven 3.9+
- Sample App: [`springboot_simplelogin`](https://github.com/savitharaghunathan/springboot_simplelogin)
- Kai VSCode IDE Extension `v0.1.0`

## Step 1: Set Up Environment

### 1.1 Clone the Sample App and custom rules

```bash
git clone https://github.com/savitharaghunathan/springboot_simplelogin.git

git clone https://github.com/savitharaghunathan/custom_rules.git

```

### 1.2 Install Kai VSCode Extension

Follow the [official guide](https://github.com/konveyor/kai/blob/main/docs/installation.md) for installation instructions.

### 1.3 Configure Kai

<TODO add screenshots for configure option>

Your VSCode settings.json should look like this,

```yaml
{
  "konveyor.analysis.labelSelector": "(konveyor.io/target=cloud-readiness || konveyor.io/target=jakarta-ee || konveyor.io/target=openjdk17) || (konveyor.io/target=spring-boot3+) || (discovery)",
  "konveyor.analysis.customRules":
    ["<your path to custom_rules for this application>/springlogin"],
  "konveyor.analysis.useDefaultRulesets": true,
}
```

Once you are done with the configuration, start the analyzer via the Kai analyzer panel.

<add screen shot>

## Step 2: Understand the Custom Rules

Before we run the analysis, let’s understand the custom rules we are going to use for migrating from Spring Boot 2 to Spring Boot 3, focusing specifically on the removal of `WebSecurityConfigurerAdapter` and discouraged configuration overrides.

### 2.1. Custom Rule for Deprecated configure(AuthenticationManagerBuilder) Method

The `SecurityConfig.java` class configures users and roles using the now-discouraged configure `(AuthenticationManagerBuilder auth)` method:

#### Before Migration

```java

@Override
protected void configure(AuthenticationManagerBuilder auth) throws Exception {
    auth.inMemoryAuthentication()
        .withUser("user").password(passwordEncoder().encode("userpass")).roles("USER")
        .and()
        .withUser("admin").password(passwordEncoder().encode("adminpass")).roles("ADMIN");

    System.out.println("Encoded userpass: " + passwordEncoder().encode("userpass"));
}
```

##### Problem

Overriding `configure(AuthenticationManagerBuilder)` is discouraged in Spring Security 5.7 and won't work in Spring Boot 3/Spring 6, because `WebSecurityConfigurerAdapter` is removed.

##### Solution

Define a separate `UserDetailsService bean` to configure in-memory authentication. This approach aligns with the modular, bean-based style recommended in Spring Boot 3+

#### After Migration

```java
@Bean
public UserDetailsService userDetailsService(PasswordEncoder encoder) {
    InMemoryUserDetailsManager manager = new InMemoryUserDetailsManager();
    manager.createUser(User.withUsername("user")
        .password(encoder.encode("userpass"))
        .roles("USER").build());
    manager.createUser(User.withUsername("admin")
        .password(encoder.encode("adminpass"))
        .roles("ADMIN").build());
    return manager;
}
```

#### Corresponding custom rule

````yaml
- ruleID: spring-security-replace-authenticationmanagerbuilder-00001
  description: configure(AuthenticationManagerBuilder) override is discouraged since Spring Security 5.7.
  category: mandatory
  effort: 2
  labels:
    - konveyor.io/source=spring-boot2
    - konveyor.io/target=spring-boot3+
  when:
    java.referenced:
      location: METHOD
      pattern: configure(org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder) *
  message: |
    Overriding `configure(AuthenticationManagerBuilder)` is **discouraged** in Spring Security 5.7.
    Instead, define a `UserDetailsService` and `PasswordEncoder` bean.

    **Fix:** Move user setup into a `UserDetailsService` bean like this:

    ```java
    @Bean
    public UserDetailsService userDetailsService(PasswordEncoder encoder) {
        InMemoryUserDetailsManager manager = new InMemoryUserDetailsManager();
        manager.createUser(User.withUsername("user")
            .password(encoder.encode("userpass"))
            .roles("USER").build());
        manager.createUser(User.withUsername("admin")
            .password(encoder.encode("adminpass"))
            .roles("ADMIN").build());
        return manager;
    }
    ```

  links:
    - title: "Spring Blog - Security without WebSecurityConfigurerAdapter"
      url: https://spring.io/blog/2022/02/21/spring-security-without-the-websecurityconfigureradapter
````

### 2.2. Custom Rule for Deprecated configure(HttpSecurity) Method

The class also overrides the configure(HttpSecurity http) method to define security rules,
login flow, and redirects

#### Before Migration

```java
@Override
protected void configure(HttpSecurity http) throws Exception {
    http
        .authorizeRequests()
            .antMatchers("/admin").hasRole("ADMIN")
            .antMatchers("/user").hasRole("USER")
            .anyRequest().permitAll()
        .and()
        .formLogin()
            .loginPage("/login").permitAll()
            .successHandler(customAuthenticationSuccessHandler())
        .and()
        .logout().permitAll();
}
```

##### Problem

Overriding `configure(HttpSecurity)` is discouraged in Spring Security 5.7. This approach is no longer recommended due to the deprecation of `WebSecurityConfigurerAdapter` in Spring Boot 3+.

##### Solution

Declare a `SecurityFilterChain` bean to define all your security logic. Additionally, update `antMatchers()` to `requestMatchers()` in Spring Security 6+.

#### Updated Code (After Migration)

```java
@Bean
public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/admin").hasRole("ADMIN")
            .requestMatchers("/user").hasRole("USER")
            .anyRequest().permitAll()
        )
        .formLogin(form -> form
            .loginPage("/login").permitAll()
            .successHandler(customAuthenticationSuccessHandler())
        )
        .logout(logout -> logout.permitAll());

    return http.build();
}
```

#### custom rule

````yaml
- ruleID: spring-security-replace-httpsecurity-configure-00002
  description: configure(HttpSecurity) override is discouraged since Spring Security 5.7
  category: mandatory
  effort: 2
  labels:
    - konveyor.io/source=spring-boot2
    - konveyor.io/target=spring-boot3+
  when:
    java.referenced:
      location: METHOD
      pattern: configure(org.springframework.security.config.annotation.web.builders.HttpSecurity) *
  message: |
    Overriding `configure(HttpSecurity)` is **discouraged** in Spring Security 5.7.
    Replace it by declaring a `SecurityFilterChain` bean.

    **Fix:**
    ```java
    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/admin").hasRole("ADMIN")
                .requestMatchers("/user").hasRole("USER")
                .anyRequest().permitAll()
            )
            .formLogin(form -> form
                .loginPage("/login").permitAll()
                .successHandler(customAuthenticationSuccessHandler())
            )
            .logout(logout -> logout.permitAll());

        return http.build();
    }
    ```

    preferred import - `import org.springframework.security.web.SecurityFilterChain;`

  links:
    - title: "Spring Blog - Security without WebSecurityConfigurerAdapter"
      url: https://spring.io/blog/2022/02/21/spring-security-without-the-websecurityconfigureradapter
````

You can learn more about writing your own custom rules [here](https://github.com/konveyor/kai/blob/main/docs/custom_ruleset.md).

## Step 3: Run Analysis

<TODO>

| **Area**             | **Old Usage**                                                             | **New Recommended Pattern**                              |
| -------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------- |
| Authentication setup | `configure(AuthenticationManagerBuilder)` with `inMemoryAuthentication()` | `@Bean UserDetailsService`                               |
| Security rules       | `configure(HttpSecurity)`                                                 | `@Bean SecurityFilterChain`                              |
| Endpoint matchers    | `antMatchers("/admin")`                                                   | `requestMatchers("/admin")`                              |
| Class structure      | `extends WebSecurityConfigurerAdapter`                                    | No inheritance. configuration is based on bean injection |

## 4. Run the app

<TODO>

## Conclusion

<TODO>
