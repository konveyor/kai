# Konveyor AI Service

This utility provides a service to generate AI prompts based off of a solved example and source that requires updating. It also proxies requests to LLMs, and will likely include additional functionality as required.

## Usage

To deploy in cluster:

oc create configmap models --from-file kai.conf.d
oc new-app quay.io/jmontleon/kai-service:latest
oc set volumes deploy/kai-service --add --type configmap -m /usr/local/etc/kai.conf.d --configmap-name kai-conf --name models
oc patch deploy/kai-service --patch '{"spec":{"template":{"metadata":{"labels":{"role":"tackle-ui"}}}}}' --type=merge
oc create route edge kai-service --service kai-service --insecure-policy Redirect

## Brief Examples

### Generate a Prompt

```bash
curl -k 'https://kai-service-konveyor-tackle.apps.example.com/generate_prompt' -X POST -H "Content-Type: application/json" -d '{ "issue_description": "my bad description",
                                                                                                                                             "language": "java-python-go-whatever",
                                                                                                                                             "example_original_code": "my original code",
                                                                                                                                             "example_solved_code": "my solved example",
                                                                                                                                             "current_original_code": "my current issue code",
                                                                                                                                             "model_template": "gpt" }'
```

### Proxy a Request

```bash
export OPENAI_API_KEY=replace-with-your-key
curl -k 'https://kai-service-konveyor-tackle.apps.example.com/proxy?upstream_url=https://api.openai.com/v1/chat/completions' \
-X POST -H "Content-Type: application/json" -H "Authorization: Bearer $OPENAI_API_KEY" -d '{ "stream": true, "model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Say this is a test!"}] }'
```
