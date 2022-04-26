# Shackled-C4D-Plugin
A plugin for Cinema 4D to allow you to export objects to the Shackled on-chain rendering engine.

Shackled Creator: https://shackled.spectra.art/#/creator

Original Blender File w/ Script Pre-Loaded: [Here](https://shackled-frontend81451-dev.s3.amazonaws.com/public/render_docs/shackled.blend)

## Requirements

- Cinema 4D Studio version or a triangulated mesh already

## Installation

1. Download the `ShackledExport.py` file from the repo above.
2. Open Cinema4D
3. Under the Script Tab, hover over User Scripts, select the "Scripts Folder" option.
4. This should open up your explorer to show the scripts folder. Drop the `ShackledExport.py` file into there.
5. Under the Script Tab, select the "Script Manager" option.
6. In the Script dropdown at the top, select ShackledExport if it's not already selected.
7. Change the `output_folder` variable to the folder you want to export your Shackled jsons to.

## Exporting Objects

First, select your object and under the "Mesh" tab, hover over "Commands" and select the "Retriangulate" option. This is required for the object to be rendered correctly on-chain.

Second, add a Vertex Paint tag to your objects that you want to export. This will allow you to color the object for the Shackled Renderer. Refer to the Youtube video linked up top for more details on how to use Vertex Paint. If you don't include a Vertex Paint tag, your object will be exported as a red object by default.

Finally, click Execute on the Script Manager window you opened earlier. If you don't have it open but already setup the output folder, simply click the "ShackledExport" option under User Scripts in the "Script" tab.

This should export your object into a JSON file which you can find with the same name as the object in the heiracrchy. This will overwrite any objects named the same thing so make sure they are all unique!

If you run into an error, under the "Script" tab, select the "Console" option.
