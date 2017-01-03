#
# Autogenerated by Frugal Compiler (2.0.0-RC5)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#



import asyncio
from datetime import timedelta
import inspect

from frugal.aio.processor import FBaseProcessor
from frugal.aio.processor import FProcessorFunction
from frugal.exceptions import FApplicationException
from frugal.exceptions import FMessageSizeException
from frugal.exceptions import FTimeoutException
from frugal.middleware import Method
from frugal.transport import TMemoryOutputBuffer
from thrift.Thrift import TApplicationException
from thrift.Thrift import TMessageType
from . import f_BasePinger
from .ttypes import *


class Iface(f_BasePinger.Iface):

    async def ping(self, ctx):
        """
        Args:
            ctx: FContext
        """
        pass


class Client(f_BasePinger.Client, Iface):

    def __init__(self, provider, middleware=None):
        """
        Create a new Client with an FServiceProvider containing a transport
        and protocol factory.

        Args:
            provider: FServiceProvider
            middleware: ServiceMiddleware or list of ServiceMiddleware
        """
        middleware = middleware or []
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]
        super(Client, self).__init__(provider, middleware=middleware)
        middleware += provider.get_middleware()
        self._methods.update({
            'ping': Method(self._ping, middleware),
        })

    async def ping(self, ctx):
        """
        Args:
            ctx: FContext
        """
        return await self._methods['ping']([ctx])

    async def _ping(self, ctx):
        timeout = ctx.timeout / 1000.0
        future = asyncio.Future()
        timed_future = asyncio.wait_for(future, timeout)
        await self._transport.register(ctx, self._recv_ping(ctx, future))
        try:
            await self._send_ping(ctx)
            result = await timed_future
        except asyncio.TimeoutError:
            raise FTimeoutException('ping timed out after {} milliseconds'.format(ctx.timeout))
        finally:
            await self._transport.unregister(ctx)
        return result

    async def _send_ping(self, ctx):
        buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('ping', TMessageType.CALL, 0)
        args = ping_args()
        args.write(oprot)
        oprot.writeMessageEnd()
        await self._transport.send(buffer.getvalue())

    def _recv_ping(self, ctx, future):
        def ping_callback(transport):
            iprot = self._protocol_factory.get_protocol(transport)
            iprot.read_response_headers(ctx)
            _, mtype, _ = iprot.readMessageBegin()
            if mtype == TMessageType.EXCEPTION:
                x = TApplicationException()
                x.read(iprot)
                iprot.readMessageEnd()
                if x.type == FApplicationException.RESPONSE_TOO_LARGE:
                    future.set_exception(FMessageSizeException.response(x.message))
                    return
                future.set_exception(x)
                return
            result = ping_result()
            result.read(iprot)
            iprot.readMessageEnd()
            future.set_result(None)
        return ping_callback


class Processor(f_BasePinger.Processor):

    def __init__(self, handler, middleware=None):
        """
        Create a new Processor.

        Args:
            handler: Iface
        """
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]

        super(Processor, self).__init__(handler, middleware=middleware)
        self.add_to_processor_map('ping', _ping(Method(handler.ping, middleware), self.get_write_lock()))


class _ping(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_ping, self).__init__(handler, lock)

    async def process(self, ctx, iprot, oprot):
        args = ping_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = ping_result()
        try:
            ret = self._handler([ctx])
            if inspect.iscoroutine(ret):
                ret = await ret
        except TApplicationException as ex:
            async with self._lock:
                _write_application_exception(ctx, oprot, "ping", exception=ex)
                return
        except Exception as e:
            async with self._lock:
                e = _write_application_exception(ctx, oprot, "ping", type=TApplicationException.UNKNOWN, message=e.args[0])
            raise e from None
        async with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('ping', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except FMessageSizeException as e:
                raise _write_application_exception(ctx, oprot, "ping", type=FApplicationException.RESPONSE_TOO_LARGE, message=e.args[0])


def _write_application_exception(ctx, oprot, method, type=None, message=None, exception=None):
    if exception is not None:
        x = exception
    else:
        x = TApplicationException(type=typ, message=message)
    oprot.write_response_headers(ctx)
    oprot.writeMessageBegin(method, TMessageType.EXCEPTION, 0)
    x.write(oprot)
    oprot.writeMessageEnd()
    oprot.get_transport().flush()
    return x

class ping_args(object):
    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('ping_args')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class ping_result(object):
    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('ping_result')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

