# TourChina
## iOS application for [TourChina]

### Description
Multiclass image classification of China landmarks.


### Dependencies

- Swift 4
- iOS 11.2 SDK / iOS 11.1 SDK
- Xcode 9.2 / 9.1
- macOS 10.13.1+

### Supported devices and platforms
- Any device running iOS 11.1+

### Usage
- Create a Single view iOS app in Xcode with camera view.
- Add the coreml model you got from training or if you skipped training, download the mlmodel from release section of the repo. 
- Initiate the model inside your swift code and run inference on images captured or in the way you have defined image input on your app.
- If you wish to use the existing app, just import the mlmodel into project directory and build.
- Best if you can test on a device instead of an emulator.


### References

- [Classifying Images with Vision and Core ML](https://developer.apple.com/documentation/vision/classifying_images_with_vision_and_core_ml)
- [Turi Create README](https://github.com/apple/turicreate)
