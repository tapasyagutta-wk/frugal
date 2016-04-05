// Autogenerated by Frugal Compiler (1.1.1)
// DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING

library base.src.f_basefoo_scope;

import 'dart:async';

import 'dart:typed_data' show Uint8List;
import 'package:thrift/thrift.dart' as thrift;
import 'package:frugal/frugal.dart' as frugal;

import 'package:base/base.dart' as t_base;
import 'base_foo.dart' as t_base_foo_file;


abstract class FBaseFoo {

  Future basePing(frugal.FContext ctx);
}

class FBaseFooClient implements FBaseFoo {

  FBaseFooClient(frugal.FTransport transport, frugal.FProtocolFactory protocolFactory) {
    _transport = transport;
    _transport.setRegistry(new frugal.FClientRegistry());
    _protocolFactory = protocolFactory;
    _oprot = _protocolFactory.getProtocol(_transport);
  }

  frugal.FTransport _transport;
  frugal.FProtocolFactory _protocolFactory;
  frugal.FProtocol _oprot;
  frugal.FProtocol get oprot => _oprot;

  Future basePing(frugal.FContext ctx) async {
    var controller = new StreamController();
    _transport.register(ctx, _recvBasePingHandler(ctx, controller));
    try {
      oprot.writeRequestHeader(ctx);
      oprot.writeMessageBegin(new thrift.TMessage("basePing", thrift.TMessageType.CALL, 0));
      t_base_foo_file.basePing_args args = new t_base_foo_file.basePing_args();
      args.write(oprot);
      oprot.writeMessageEnd();
      await oprot.transport.flush();
      return await controller.stream.first.timeout(ctx.timeout);
    } finally {
      _transport.unregister(ctx);
    }
  }

  _recvBasePingHandler(frugal.FContext ctx, StreamController controller) {
    basePingCallback(thrift.TTransport transport) {
      try {
        var iprot = _protocolFactory.getProtocol(transport);
        iprot.readResponseHeader(ctx);
        thrift.TMessage msg = iprot.readMessageBegin();
        if (msg.type == thrift.TMessageType.EXCEPTION) {
          thrift.TApplicationError error = thrift.TApplicationError.read(iprot);
          iprot.readMessageEnd();
          if (error.type == frugal.FTransport.RESPONSE_TOO_LARGE) {
            controller.addError(new frugal.FMessageSizeError.response());
            return;
          }
          throw error;
        }

        t_base_foo_file.basePing_result result = new t_base_foo_file.basePing_result();
        result.read(iprot);
        iprot.readMessageEnd();
        controller.add(null);
      } catch(e) {
        controller.addError(e);
        rethrow;
      }
    }
    return basePingCallback;
  }

}
