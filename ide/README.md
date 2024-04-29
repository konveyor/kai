# IDE Integration

This document captures information related to an IDE extension for VSCode the project is exploring.

The source code for the VSCode IDE plugin is here:

- https://github.com/konveyor-ecosystem/kai-vscode-plugin
  - This extension is forked from the [WindUp project](https://windup.github.io/blog/introduction/)

To make life a little easier we are carrying some builds of the plugin in the [kai/ide/vsix](/ide/vsix) directory

## Functionality Overview

The plugin will allow you to:

- Run [Kantra](https://github.com/konveyor/kantra), Konveyor's static code analysis CLI tool
- View the migration issues Kantra discovered
- Select a file and generate a code fix for the migration issues Kantra found
  - As of April 2024 the IDE will connect to a Kai instance running on localhost
  - Integration to have Kai run alongside a Konveyor instance is planned towards later portion of Summer 2024

## Installation

### Pre-requisite

#### Ensure you can run Kantra

- Please ensure you can run [Kantra](https://github.com/konveyor/kantra) from CLI of your machine. We have some example scripts to help show how to do this on MacOS via at [/samples/macos](/samples/macos)

  1. Ensure podman is running (for MacOS we need to run a podman VM): [samples/macos/restart_podman_machine.sh](/samples/macos/restart_podman_machine.sh)
  1. Fetch the Kantra binary, we will download it from a container image: [samples/macos/get_latest_kantra_cli.sh](/samples/macos/get_latest_kantra_cli.sh)

- You can run the below scripts to run an anlysis from the `example` directory:

  1. `cd example`
  1. Fetch source code to run analysis against via: [./fetch.sh](example/fetch.sh)
     - Will clone a git repo
  1. Will run Kantra to analyze the previously cloned source repo: [./analyze](example/analyze.sh)

- It is important that Kantra is able to run successfully on your machine before you proceed with the IDE extension. It will need to do a similar step of running Kantra from inside of the IDE.

#### Ensure you do NOT have an older version of MTA IDE Extension installed

- Please ensure you do NOT have a prior version of the MTA plugin installed
  ![IDE_Uninstall](images/IDE_Uninstall.png)

1. Click on IDE Extensions
1. Search for 'MTA'
1. If you have an MTA plugin installed, click 'Uninstall'
1. Restart your IDE

### Installation Steps

The below will guide you installing an engineering build of the VSCode Plugin which we have available as a `.vsix` file under [kai/ide/vsix](/ide/vsix) directory.

1. Download the latest `.vsix` we have available at [kai/ide/vsix](/ide/vsix)
1. Click on IDE Extensions tab on left side
1. Look at top of the IDE Extension window and click the `...` to get a drop down window
1. Click on `Install from VSIX`
   ![Install_From_VSIX](images/Install_From_VSIX.png)
1. Select the `.vsix` file to install
1. Search the extensions and look for `MTA`.
   - As of April 2024 the extension will show as 'MTA' extension v7.0.2
1. Reload VSCode

## Using VSCode Extension

### Usage Summary

1. Open the IDE Extension panel.

   1. On the left panel you will see a list of icons below Explorer, Extensions, etc... one of those icons will say 'MTA' if you have the IDE Extension installed.
      ![Open_MTA](images/Open_MTA.png)
      - Click the MTA icon in the highlighted red square

1. Create a Configuration to Run Analysis (with Kantra)
   1. With the MTA panel open
      ![Open_Configuration](images/OpenConfiguration.png)
   1. If the configuration editor is not already open, click on the MTA configuration
      ![OpenedMTA_Configuration](images/OpenedMTA_Configuration.png) \* This is the area to configure how to run static code analysis with Kantra
1. Configure Kantra to run

   1. Specify the CLI for Kantra  
      ![CLI Option](images/CLI_Option.png)

      - You can use the Kantra binary you used earlier in pre-requisite, for example our scripts will place this at [samples/bin](kai/samples/bin)

   1. Select the Targets
      ![SelectTargets](images/MakeSelection.png)
      - Select:
        - `containerizarion`
        - `jakarta-ee`
        - `jakarta-ee8+`
        - `jakarta-ee9+`
        - `quarkus`
   1. Add custom rules
      ![CustomRules](images/CustomRules.png)

      - You can use the custom rules we supply at [samples/custom_rules](samples/custom_rules)

   1. Close the configuration editor by closing the configuration tab

1. Run the analysis

   1. Click on the triangular play button to Run the analysis
      ![AboutToRunAnalysis](images/AboutToRunAnalysis.png)
   1. Analysis will run for several minutes
      ![AnalysisRunning.png](images/AnalysisRunning.png)

1. View the discovered issues
1. Generate a fix
1. Accept or Reject changes

### Using Command Line

- Run \*\*<code>npm install -g vsce</code> </strong>in your terminal.
- Once vsce is installed, you can install the .vsix file with the following command:

```
code --install-extension path/to/your-extension.vsix

```

- Restart/reload vscode

## Prerequisite:

- Follow the instructions to install **Kantra**
  - [https://github.com/konveyor/kantra?tab=readme-ov-file#analyze](https://github.com/konveyor/kantra?tab=readme-ov-file#analyze)
- Follow the instructions to install **KAI**
  - **[https://github.com/konveyor-ecosystem/kai?tab=readme-ov-file#demo-pre-requisites](https://github.com/konveyor-ecosystem/kai?tab=readme-ov-file#demo-pre-requisites)**
  - Follow the steps to setup backend
- Install Cool-store app

## Step:1 Run Kantra Analysis

- Open vscode and Navigate to** File > Open, **locate to folder we just cloned **EAP-COOLSTORE-MONOLITH **

<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image4.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image4.png "image_tooltip")

- Navigate to MTA plugin

<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image5.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image5.png "image_tooltip")

- Select the configuration params as shown below:
  - Input: path to coolstore app
  - CLI: kantra
  - target : ,containerization, jakarta-ee, jakarta-ee8+, jakarta-ee9+, quarkus (if the target is unavailable in the list, Click “Add” button, type your target and hit enter )

<p id="gdcalert6" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image6.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert7">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image6.png "image_tooltip")

    * rules: Navigate to PATH shown below [https://github.com/konveyor-ecosystem/kai/tree/main/samples/custom_rules](https://github.com/konveyor-ecosystem/kai/tree/main/samples/custom_rules)

<p id="gdcalert7" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image7.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert8">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image7.png "image_tooltip")

- Click the Run button to run the analysis
- Wait till Analysis is Completed successfully. (Expect ~2-3 minutes to complete)

<p id="gdcalert8" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image8.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert9">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image8.png "image_tooltip")

## Step: 2 Run Kai-Fix

- Make Sure your kai backed is running
- To Fix all the Incidents or the file, **Right Click** on the file > **Kai-Fix All**

<p id="gdcalert9" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image9.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert10">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image9.png "image_tooltip")

- To Fix the single Incident,** Right Click** on the Incident > **Generate Kai-Fix**

<p id="gdcalert10" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image10.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert11">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image10.png "image_tooltip")

- Fix can take pu some time, look at the indicator

<p id="gdcalert11" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image11.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert12">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image11.png "image_tooltip")

- After the fix is generated, proposed changes will appear on the right side of the diff editor, while the left side displays the original file, which is not editable. If you find the proposed changes unconvincing, you have the option to revert them by clicking (→).
- For more detailed explanations, refer to the Output channel in the horizontal panel below the diff editor.
- Clicking "Accept Changes" will save the proposed changes and replace the original file. Selecting "Reject Changes" will discard the proposed changes and close the editor.

<p id="gdcalert12" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image12.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert13">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>

![alt_text](images/image12.png "image_tooltip")
