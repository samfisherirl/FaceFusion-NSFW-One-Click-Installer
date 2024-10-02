# Forked From https://github.com/facefusion/facefusion

Thanks henry for all the work.

## CURRENTLY NOT FUNCTIONAL FOR V3 *

Working on update.

Download working version for[ FF 2.6 here](https://github.com/samfisherirl/FaceFusion-NSFW-One-Click-Installer/tree/6921d30f82c21568353869270a86390096ef6ac8) 

This is now for use with my Docker version here: https://github.com/samfisherirl/facefusion-docker-NSFW


Same issue here. I had a look with procmon to investigate, and the problem is that onnxruntime_providers_tensorrt.dll has dependencies (imports) from the following dlls and fails to load because it is not finding them in the library load path search:

cublas64_11.dll --> CUDA 11.x
cudart64_110.dll --> CUDA 11.x
cudnn64_8.dll --> cuDNN 8.x
nvinfer_plugin.dll --> NVIDIA TensorRT
nvinfer.dll --> NVIDIA TensorRT
So this issue is because TensorRT, CUDA 11.x, or cuDNN verison 8.x is not installed or not added to path yet.

The one most commonly missing is probably TensorRT for CUDA 11.x:

https://docs.nvidia.com/deeplearning/tensorrt/install-guide/index.html
NOTE: Requires a specific version of cuDNN (currently cuDNN 8.6.0)
Then download TensorRT library from https://developer.nvidia.com/tensorrt
Make sure to add the lib folder to path.
Install CUDA 11.x:
https://developer.nvidia.com/cuda-downloads

CuDNN 8.x for CUDA 11.x, matching the above TensorRT version requirement:
https://developer.nvidia.com/cudnn

And don't forget them to add all the /bin and /lib folders that have all the dlls to your PATH system environment variables and restart your terminal.

My issue was installing TensorRT and adding it to path, this fixed it to get the next error for me.

Upon running, it eventually got to a different error stating that TensorRT was linked to cuDNN 8.6.0, while I had cuDNN 8.3.0 installed. The next step was adding cuDNN 8.6.0 as well, and making sure it's path was before my older version. You have click the "Archive" button on the cuDNN download page to see all versions.

Hope this helps someone!
