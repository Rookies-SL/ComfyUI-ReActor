
# ReActor Nodes for ComfyUI

## Installation

### Standalone (Portable) <a href="https://github.com/comfyanonymous/ComfyUI">ComfyUI</a> for Windows

1. Choose between two options:
   - (ComfyUI Manager) Open ComfyUI Manager, click "Install Custom Nodes", type "ReActor" in the "Search" field and then click "Install". After ComfyUI will complete the process - please restart the Server.
   - (Manually) Go to `ComfyUI\custom_nodes`, open Console and run `git clone https://github.com/Gourieff/ComfyUI-ReActor`
2. Go to `ComfyUI\custom_nodes\ComfyUI-ReActor` and run `install.bat`
3. Download required models from the Section below
4. Run ComfyUI and find there ReActor Nodes inside the menu `ReActor` or by using a search


## Models

 - buffalo_l: downloaded on first launch into `ComfyUI\models\insightface\models\buffalo_l`, or you can download manually from [here](https://huggingface.co/datasets/Gourieff/ReActor/tree/main/models)
 - inswapper_128: downloaded during installation into `ComfyUI\models\insightface`, or you can download manually from [here](https://huggingface.co/datasets/Gourieff/ReActor/tree/main/models)
 - reswapper_128/256: https://huggingface.co/datasets/Gourieff/ReActor/tree/main/models put them into `ComfyUI\models\reswapper`
 - hyperswap_256: https://huggingface.co/facefusion/models-3.3.0/tree/main (hyperswap_1a_256.onnx, hyperswap_1b_256.onnx, hyperswap_1a_256.onnx) put them into `ComfyUI\models\hyperswap`
 - Face restoration models: https://huggingface.co/datasets/Gourieff/ReActor/tree/main/models/facerestore_models put any you like into `ComfyUI\models\facerestore_models`
 - Ultralytics model: https://huggingface.co/datasets/Gourieff/ReActor/blob/main/models/detection/bbox/face_yolov8m.pt put into `ComfyUI\models\ultralytics\bbox`
 - SAM models: https://huggingface.co/datasets/Gourieff/ReActor/tree/main/models/sams put into `ComfyUI\models\sams`

## Usage

You can find ReActor Nodes inside the menu `ReActor` or by using a search (just type "ReActor" in the search field)

List of Nodes:
- ••• Main Nodes •••
  - ReActorFaceSwap (Main Node)
  - ReActorFaceSwapOpt (Main Node with the additional Options input)
  - ReActorOptions (Options for ReActorFaceSwapOpt)
  - ReActorFaceBoost (Face Booster Node)
  - ReActorMaskHelper (Masking Helper)
  - ReActorSetWeight (Set Face Swap Weight)
- ••• Operations with Face Models •••
  - ReActorSaveFaceModel (Save Face Model)
  - ReActorLoadFaceModel (Load Face Model)
  - ReActorBuildFaceModel (Build Blended Face Model)
  - ReActorMakeFaceModelBatch (Make Face Model Batch)
- ••• Additional Nodes •••
  - ReActorRestoreFace (Face Restoration)
  - ReActorRestoreFaceAdvanced (Restore Face Advanced)
  - ReActorFaceSimilarity (Face Similarity)
  - ReActorImageDublicator (Dublicate one Image to Images List)
  - ImageRGBA2RGB (Convert RGBA to RGB)
  - ReActorUnload (Unload ReActor models from VRAM)

Connect all required slots and run the query.

### Main Node Inputs

- `input_image` - is an image to be processed (target image, analog of "target image" in the SD WebUI extension);
  - Supported Nodes: "Load Image", "Load Video" or any other nodes providing images as an output;
- `source_image` - is an image with a face or faces to swap in the `input_image` (source image, analog of "source image" in the SD WebUI extension);
  - Supported Nodes: "Load Image" or any other nodes providing images as an output;
- `face_model` - is the input for the "Load Face Model" Node or another ReActor node to provide a face model file (face embedding) you created earlier via the "Save Face Model" Node;
  - Supported Nodes: "Load Face Model", "Build Blended Face Model";
- `options` - to connect ReActorOptions;
  - Supported Nodes: "ReActorOptions";
- `face_boost` - to connect ReActorFaceBoost;
  - Supported Nodes: "ReActorFaceBoost";

### Main Node Outputs

- `IMAGE` - is an output with the resulted image;
  - Supported Nodes: any nodes which have images as an input;
- `FACE_MODEL` - is an output providing a source face's model being built during the swapping process;
  - Supported Nodes: "Save Face Model", "ReActor", "Make Face Model Batch";
- `ORIGINAL_IMAGE` - `input_image` bypass;

### Face Restoration

Since version 0.3.0 ReActor Node has a buil-in face restoration.<br>Just download the models you want (see [Installation](#installation) instruction) and select one of them to restore the resulting face(s) during the faceswap. It will enhance face details and make your result more accurate.

### Face Indexes

By default ReActor detects faces in images from "large" to "small".<br>You can change this option by adding ReActorFaceSwapOpt node with ReActorOptions.

And if you need to specify faces, you can set indexes for source and input images.

Index of the first detected face is 0.

You can set indexes in the order you need.<br>
E.g.: 0,1,2 (for Source); 1,0,2 (for Input).<br>This means: the second Input face (index = 1) will be swapped by the first Source face (index = 0) and so on.

### Genders

You can specify the gender to detect in images.<br>
ReActor will swap a face only if it meets the given condition.

### Face Models

Since version 0.4.0 you can save face models as "safetensors" files (stored in `ComfyUI\models\reactor\faces`) and load them into ReActor implementing different scenarios and keeping super lightweight face models of the faces you use.

To make new models appear in the list of the "Load Face Model" Node - just refresh the page of your ComfyUI web application.<br>
(I recommend you to use ComfyUI Manager - otherwise you workflow can be lost after you refresh the page if you didn't save it before that).

### Masking Helper

Face Masking feature is available since version 0.5.0, just add the "ReActorMaskHelper" Node to the workflow and connect it as shown below:

<img src="https://github.com/Gourieff/Assets/blob/main/comfyui-reactor-node/0.5.0-whatsnew-01.jpg?raw=true" alt="0.5.0-whatsnew-01" width="100%"/>

If you don't have the "face_yolov8m.pt" Ultralytics model - you can download it from the [Assets](https://huggingface.co/datasets/Gourieff/ReActor/blob/main/models/detection/bbox/face_yolov8m.pt) and put it into the "ComfyUI\models\ultralytics\bbox" directory
<br>
As well as ["sam_vit_b_01ec64.pth"](https://huggingface.co/datasets/Gourieff/ReActor/blob/main/models/sams/sam_vit_b_01ec64.pth) or ["sam_vit_l_0b3195.pth"](https://huggingface.co/datasets/Gourieff/ReActor/blob/main/models/sams/sam_vit_l_0b3195.pth) (better occlusion) - download (if you don't have it) and put it into the "ComfyUI\models\sams" directory;

Use this Node to gain the best results of the face swapping process:

<img src="https://github.com/Gourieff/Assets/blob/main/comfyui-reactor-node/0.5.0-whatsnew-02.jpg?raw=true" alt="0.5.0-whatsnew-02" width="100%"/>

### Face Swap Weigth

You can set the strength of face swap for `source_image` or `face_model` from 0% to 100% (in 12.5% step) with `ReActorSetWeight` node

<center>
<img src="https://github.com/Gourieff/Assets/blob/main/comfyui-reactor-node/0.6.0-whatsnew-01.jpg?raw=true" alt="0.6.0-whatsnew-01" width="100%"/>
</center>

## Troubleshooting

### **I. "AttributeError: 'NoneType' object has no attribute 'get'"**

This error may occur if there's smth wrong with the model file `inswapper_128.onnx`

Try to download it manually from [here](https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/inswapper_128.onnx)
and put it to the `ComfyUI\models\insightface` replacing existing one

### **II. "reactor.execute() got an unexpected keyword argument 'reference_image'"**

This means that input points have been changed with the latest update<br>
Remove the current ReActor Node from your workflow and add it again

### **III. "fatal: fetch-pack: invalid index-pack output" when you try to `git clone` the repository"**

Try to clone with `--depth=1` (last commit only):

     git clone --depth=1 https://github.com/Gourieff/ComfyUI-ReActor

Then retrieve the rest (if you need):

     git fetch --unshallow

## Updating

Just put .bat or .sh script from this [Repo](https://github.com/Gourieff/sd-webui-extensions-updater) to the `ComfyUI\custom_nodes` directory and run it when you need to check for updates

### Disclaimer

This software is meant to be a productive contribution to the rapidly growing AI-generated media industry. It will help artists with tasks such as animating a custom character or using the character as a model for clothing etc.

The developers of this software are aware of its possible unethical applications and are committed to take preventative measures against them. We will continue to develop this project in the positive direction while adhering to law and ethics.

Users of this software are expected to use this software responsibly while abiding the local law. If face of a real person is being used, users are suggested to get consent from the concerned person and clearly mention that it is a deepfake when posting content online. **Developers and Contributors of this software are not responsible for actions of end-users.**

By using this extension you are agree not to create any content that:
- violates any laws;
- causes any harm to a person or persons;
- propagates (spreads) any information (both public or personal) or images (both public or personal) which could be meant for harm;
- spreads misinformation;
- targets vulnerable groups of people.

This software utilizes the pre-trained models `buffalo_l` and `inswapper_128.onnx`, which are provided by [InsightFace](https://github.com/deepinsight/insightface/). These models are included under the following conditions:

[From insighface license](https://github.com/deepinsight/insightface/tree/master/python-package): The InsightFace’s pre-trained models are available for non-commercial research purposes only. This includes both auto-downloading models and manually downloaded models.

Users of this software must strictly adhere to these conditions of use. The developers and maintainers of this software are not responsible for any misuse of InsightFace’s pre-trained models.

Please note that if you intend to use this software for any commercial purposes, you will need to train your own models or find models that can be used commercially.

### Models Hashsum

#### Safe-to-use models have the following hash:

inswapper_128.onnx
```
MD5:a3a155b90354160350efd66fed6b3d80
SHA256:e4a3f08c753cb72d04e10aa0f7dbe3deebbf39567d4ead6dce08e98aa49e16af
```

1k3d68.onnx

```
MD5:6fb94fcdb0055e3638bf9158e6a108f4
SHA256:df5c06b8a0c12e422b2ed8947b8869faa4105387f199c477af038aa01f9a45cc
```

2d106det.onnx

```
MD5:a3613ef9eb3662b4ef88eb90db1fcf26
SHA256:f001b856447c413801ef5c42091ed0cd516fcd21f2d6b79635b1e733a7109dbf
```

det_10g.onnx

```
MD5:4c10eef5c9e168357a16fdd580fa8371
SHA256:5838f7fe053675b1c7a08b633df49e7af5495cee0493c7dcf6697200b85b5b91
```

genderage.onnx

```
MD5:81c77ba87ab38163b0dec6b26f8e2af2
SHA256:4fde69b1c810857b88c64a335084f1c3fe8f01246c9a191b48c7bb756d6652fb
```

w600k_r50.onnx

```
MD5:80248d427976241cbd1343889ed132b3
SHA256:4c06341c33c2ca1f86781dab0e829f88ad5b64be9fba56e56bc9ebdefc619e43
```

**Please check hashsums if you download these models from unverified (or untrusted) sources**

<a name="credits">

## Thanks and Credits

<details>
	<summary><a>Click to expand</a></summary>

<br>

|file|source|license|
|----|------|-------|
|[buffalo_l.zip](https://huggingface.co/datasets/Gourieff/ReActor/blob/main/models/buffalo_l.zip) | [DeepInsight](https://github.com/deepinsight/insightface) | ![license](https://img.shields.io/badge/license-non_commercial-red) |
| [codeformer-v0.1.0.pth](https://huggingface.co/datasets/Gourieff/ReActor/blob/main/models/facerestore_models/codeformer-v0.1.0.pth) | [sczhou](https://github.com/sczhou/CodeFormer) | ![license](https://img.shields.io/badge/license-non_commercial-red) |
| [GFPGANv1.3.pth](https://huggingface.co/datasets/Gourieff/ReActor/blob/main/models/facerestore_models/GFPGANv1.3.pth) | [TencentARC](https://github.com/TencentARC/GFPGAN) | ![license](https://img.shields.io/badge/license-Apache_2.0-green.svg) |
| [GFPGANv1.4.pth](https://huggingface.co/datasets/Gourieff/ReActor/blob/main/models/facerestore_models/GFPGANv1.4.pth) | [TencentARC](https://github.com/TencentARC/GFPGAN) | ![license](https://img.shields.io/badge/license-Apache_2.0-green.svg) |
| [inswapper_128.onnx](https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/inswapper_128.onnx) | [DeepInsight](https://github.com/deepinsight/insightface) | ![license](https://img.shields.io/badge/license-non_commercial-red) |
| [inswapper_128_fp16.onnx](https://huggingface.co/datasets/Gourieff/ReActor/resolve/main/models/inswapper_128_fp16.onnx) | [Hillobar](https://github.com/Hillobar/Rope) | ![license](https://img.shields.io/badge/license-non_commercial-red) |

[BasicSR](https://github.com/XPixelGroup/BasicSR) - [@XPixelGroup](https://github.com/XPixelGroup) <br>
[facexlib](https://github.com/xinntao/facexlib) - [@xinntao](https://github.com/xinntao) <br>

[@s0md3v](https://github.com/s0md3v), [@henryruhs](https://github.com/henryruhs) - the original Roop App <br>
[@ssitu](https://github.com/ssitu) - the first version of [ComfyUI_roop](https://github.com/ssitu/ComfyUI_roop) extension

</details>

<a name="note">

### Note!

**If you encounter any errors when you use ReActor Node - don't rush to open an issue, first try to remove current ReActor node in your workflow and add it again**

**ReActor Node gets updates from time to time, new functions appear and old node can work with errors or not work at all**
