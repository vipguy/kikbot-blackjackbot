# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: abtesting/v1/ab_testing_shared.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import kik_unofficial.protobuf.protobuf_validation_pb2 as protobuf__validation__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$abtesting/v1/ab_testing_shared.proto\x12\x13\x63ommon.abtesting.v1\x1a\x19protobuf_validation.proto\"i\n\nExperiment\x12\x19\n\x04name\x18\x01 \x01(\tB\x0b\xca\x9d%\x07\x08\x01(\x01\x30\xff\x01\x12\x1c\n\x07variant\x18\x02 \x01(\tB\x0b\xca\x9d%\x07\x08\x01(\x01\x30\xff\x01\x12\"\n\rexperiment_id\x18\x03 \x01(\tB\x0b\xca\x9d%\x07\x08\x00(\x00\x30\xff\x01\x42r\n\x15\x63om.kik.abtesting.rpcZRgithub.com/kikinteractive/xiphias-model-common/generated/go/abtesting/v1;abtesting\xa2\x02\x04XIABb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'abtesting.v1.ab_testing_shared_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\025com.kik.abtesting.rpcZRgithub.com/kikinteractive/xiphias-model-common/generated/go/abtesting/v1;abtesting\242\002\004XIAB'
  _EXPERIMENT.fields_by_name['name']._options = None
  _EXPERIMENT.fields_by_name['name']._serialized_options = b'\312\235%\007\010\001(\0010\377\001'
  _EXPERIMENT.fields_by_name['variant']._options = None
  _EXPERIMENT.fields_by_name['variant']._serialized_options = b'\312\235%\007\010\001(\0010\377\001'
  _EXPERIMENT.fields_by_name['experiment_id']._options = None
  _EXPERIMENT.fields_by_name['experiment_id']._serialized_options = b'\312\235%\007\010\000(\0000\377\001'
  _EXPERIMENT._serialized_start=88
  _EXPERIMENT._serialized_end=193
# @@protoc_insertion_point(module_scope)