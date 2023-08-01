import tensorflow as tf
print(tf.test.is_built_with_cuda())

print(tf.config.list_physical_devices('GPU'))
#tf.test.is_gpu_available('GPU') 위의 함수로 바뀐다고 함 (2.4.0)
print(tf.sysconfig.get_build_info())
