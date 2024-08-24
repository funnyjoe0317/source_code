import tensorflow as tf
import tensorflow_model_optimization as tfmot
from tensorflow import keras
#from solvers.NAFNet.plane_arch import PlaneNet_original, PlaneNet_original_pad, PlaneNet_original_pad_dynamic
from solvers.NAFNet.plane_arch import PlaneNet_original, PlaneNet_denoise

from solvers.networks.devblock import WsConv2D
from solvers.networks.repblock import RepBlock
from solvers.solver import DefaultOutputQuantizeConfig, NoOpQuantizeConfig, Conv2DxQuantizeConfig, DepthwiseConv2DQuantizeConfig, DefaultBNQuantizeConfig, RepBlockQuantizeConfig

import os
import cv2
import numpy as np

#os.environ['CUDA_VISIBLE_DEVICES'] = '0'

def cfg_quantization(layer):
    print(layer.name)
    if 'clip_func' in layer.name:
        print('--> clip_func done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'pad_func' in layer.name:
        print('--> pad_func done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'depth_to_space' in layer.name:
        print('--> depth_to_space done')
        #return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if 'lambda' in layer.name:
        print('--> lambda done, but you should check quantization config!!')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if 'rescaling' in layer.name:
        print('--> rescaling done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if 'ws_conv2d' in layer.name:
        print('--> ws done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=Conv2DxQuantizeConfig())
    if isinstance(layer, tf.keras.layers.Conv2D):
        print('--> cv done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=Conv2DxQuantizeConfig())
    if isinstance(layer, tf.keras.layers.DepthwiseConv2D):
        print('--> dw-cv done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DepthwiseConv2DQuantizeConfig())
    if isinstance(layer, tf.keras.layers.BatchNormalization):
        print('--> BN done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultBNQuantizeConfig())
    if 'concatenate' in layer.name:
        print('--> cc done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'rep_block' in layer.name:
        print('--> rb done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=RepBlockQuantizeConfig())
    if 'multiply' in layer.name:
        print('--> multiply done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'add' in layer.name:
        print('--> add done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'global_average_pooling2' in layer.name:
        print('--> global_average_pooling2 done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())
    if 'up_sampling2d' in layer.name:
        print('--> UpSampling2D done, but you should check quantization config!!')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if 'split' in layer.name:
        print('--> split!!')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
    if isinstance(layer, tf.keras.layers.LayerNormalization):
    #if 'layer_normalization_1' in layer.name:
        print('--> LN done')
        return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=NoOpQuantizeConfig())
        # return tfmot.quantization.keras.quantize_annotate_layer(layer, quantize_config=DefaultOutputQuantizeConfig())


    return layer

def load_qat_model(model):    
    annotate_model = tf.keras.models.clone_model(model, clone_function=cfg_quantization)
    annotate_model = tfmot.quantization.keras.quantize_annotate_model(annotate_model)
    
    with tfmot.quantization.keras.quantize_scope(
        {'NoOpQuantizeConfig': NoOpQuantizeConfig, 
         'Conv2DxQuantizeConfig': Conv2DxQuantizeConfig,
         'DepthwiseConv2DQuantizeConfig': DepthwiseConv2DQuantizeConfig,
         'WsConv2D': WsConv2D,
         'DefaultBNQuantizeConfig': DefaultBNQuantizeConfig,
         'DefaultOutputQuantizeConfig': DefaultOutputQuantizeConfig,
         'RepBlock': RepBlock,
         'RepBlockQuantizeConfig': RepBlockQuantizeConfig,
         'tf': tf}):
        
        model = tfmot.quantization.keras.quantize_apply(annotate_model)
    
    return model

# with tfmot.quantization.keras.quantize_scope(
#         {'NoOpQuantizeConfig': NoOpQuantizeConfig, 
#          'Conv2DxQuantizeConfig': Conv2DxQuantizeConfig,
#          'DepthwiseConv2DQuantizeConfig': DepthwiseConv2DQuantizeConfig,
#          'WsConv2D': WsConv2D,
#          'DefaultBNQuantizeConfig': DefaultBNQuantizeConfig,
#          'DefaultOutputQuantizeConfig': DefaultOutputQuantizeConfig,
#          'RepBlock': RepBlock,
#          'RepBlockQuantizeConfig': RepBlockQuantizeConfig,
#          'tf': tf}):
#     test = tf.keras.models.load_model('denoise_planenet_0108_QAT')
#     test.summary()

model = tf.keras.models.load_model('deblur_planenet_final')
# model = tf.keras.models.load_model('denoise_planenet_final')
model.summary()

new_model = PlaneNet_original(channels=16)
# new_model = PlaneNet_denoise(channels=16)
#new_model = load_qat_model(new_model)
new_model.set_weights(model.get_weights())
new_model.summary()
new_model.trainable = False

converter = tf.lite.TFLiteConverter.from_keras_model(new_model)
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS]
converter.target_spec.supported_types = [tf.float16]
converter.optimizations = [tf.lite.Optimize.DEFAULT]

"""
class DatasetGenerator():
    def __init__(self):
        self.dataset_dir = "./datasets/RealBlurJ/val/input"
        self.dataset_list = os.listdir(self.dataset_dir)
        
    def __call__(self):
        for dataset in self.dataset_list:
            print('representative data: {}/{}'.format(self.dataset_dir, dataset))

            #imread
            img = cv2.imread(self.dataset_dir + '/' + dataset)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            h, w, _ = img.shape
            mod_pad_h = 1080 - h
            mod_pad_w = 1920 - w
            img = cv2.copyMakeBorder(img, 0, mod_pad_h, 0, mod_pad_w, cv2.BORDER_CONSTANT, value=[0, 0, 0])

            img = img.astype(np.float32)
            img = np.expand_dims(img, 0)
            yield [img]

def representative_data_gen():
    img_array = None
    cnt = 0

    dataset_dir = "./datasets/RealBlurJ/val/input"
    dataset_list = os.listdir(dataset_dir)
    for dataset in dataset_list:
        print(self.dataset_dir + '/' + dataset)
        img = cv2.imread(dataset_dir + '/' + dataset)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        h, w, _ = img.shape
        mod_pad_h = 1080 - h
        mod_pad_w = 1920 - w
        img = cv2.copyMakeBorder(img, 0, mod_pad_h, 0, mod_pad_w, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        img = np.expand_dims(img, axis=0)
        img = img.astype(np.float32)
        
        if img_array is None:
            img_array = img
        else:
            np.append(img_array, img, axis=0)
        
        cnt += 1
        if cnt == 100:
            break
    yield [img_array]

converter = tf.lite.TFLiteConverter.from_keras_model(new_model)
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.representative_dataset = DatasetGenerator()
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8
converter.optimizations = [tf.lite.Optimize.DEFAULT]
"""

tflite_model = converter.convert()

with open('deblur_planenet_final.tflite', 'wb') as f:
# with open('denoise_planenet_final.tflite', 'wb') as f:
    f.write(tflite_model)

interpreter = tf.lite.Interpreter(model_content=tflite_model)

for input_details in interpreter.get_input_details():
    print(input_details['name'])
for output_details in interpreter.get_output_details():
    print(output_details['name'])
print(interpreter.get_signature_list())