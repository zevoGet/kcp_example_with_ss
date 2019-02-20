# encoding=utf8
from ctypes import *
import time
# 动态库
kcp_LIB = None

# 结构体1
class iqueue_head(Structure):
    pass
iqueue_head._fields_ = [
        ('next',POINTER(iqueue_head)),
        ('prev',POINTER(iqueue_head)),
    ]

# kcp 结构体
class ikcpcb(Structure):
    pass

# c端output 函数
CFoutput = CFUNCTYPE(c_int, c_char_p, c_int,POINTER(ikcpcb),c_void_p)

# c端 Log 函数
CFlog = CFUNCTYPE(None, c_char_p,POINTER(ikcpcb),POINTER(c_int))
# 结构体的域
ikcpcb._fields_ = [
    #IUINT32 conv, mtu, mss, state;
    ('conv',c_uint32),
    ('mtu',c_uint32),
    ('mss',c_uint32),
    ('state',c_uint32),

    #IUINT32 snd_una, snd_nxt, rcv_nxt;
    ('snd_una',c_uint32),
    ('snd_nxt',c_uint32),
    ('rcv_nxt',c_uint32),

    #IUINT32 ts_recent, ts_lastack, ssthresh;
    ('ts_recent',c_uint32),
    ('ts_lastack',c_uint32),
    ('ssthresh',c_uint32),

    #IINT32 rx_rttval, rx_srtt, rx_rto, rx_minrto;
    ('rx_rttval',c_int32),
    ('rx_srtt',c_int32),
    ('rx_rto',c_int32),
    ('rx_minrto',c_int32),

    #IUINT32 snd_wnd, rcv_wnd, rmt_wnd, cwnd, probe;
    ('snd_wnd',c_uint32),
    ('rcv_wnd',c_uint32),
    ('rmt_wnd',c_uint32),
    ('cwnd',c_uint32),
    ('probe',c_uint32),

    #IUINT32 current, interval, ts_flush, xmit;
    ('current',c_uint32),
    ('interval',c_uint32),
    ('ts_flush',c_uint32),
    ('xmit',c_uint32),

    #IUINT32 nrcv_buf, nsnd_buf;
    ('nrcv_buf',c_uint32),
    ('nsnd_buf',c_uint32),


    #IUINT32 nrcv_que, nsnd_que;
    ('nrcv_que', c_uint32),
    ('nsnd_que', c_uint32),

    #IUINT32 nodelay, updated;
    ('nodelay', c_uint32),
    ('updated', c_uint32),

    #IUINT32 ts_probe, probe_wait;
    ('ts_probe', c_uint32),
    ('probe_wait', c_uint32),

    #IUINT32 dead_link, incr;
    ('dead_link', c_uint32),
    ('incr', c_uint32),

    #struct IQUEUEHEAD snd_queue;
    ('snd_queue', iqueue_head),

    #struct IQUEUEHEAD rcv_queue;
    ('rcv_queue', iqueue_head),

    #struct IQUEUEHEAD snd_buf;
    ('snd_buf', iqueue_head),

    #struct IQUEUEHEAD rcv_buf;
    ('rcv_buf', iqueue_head),

    #IUINT32 *acklist;
    ('acklist', POINTER(c_uint32)),

    #IUINT32 ackcount;
    ('ackcount', c_uint32),

    #IUINT32 ackblock;
    ('ackblock', c_uint32),

    #void *user;
    ('user', c_void_p),

    #char *buffer;
    ('buffer', c_char_p),

    #int fastresend;
    ('fastresend', c_int),

    #int nocwnd, stream;
    ('nocwnd', c_int),
    ('stream', c_int),

    #int logmask;
    ('logmask', c_int),

    #int (*output)(const char *buf, int len, struct IKCPCB *kcp, void *user);
    ('output', CFoutput),

    #void (*writelog)(const char *log, struct IKCPCB *kcp, void *user);
    ('writelog', CFlog),
]

# output 函数
def outputfunc(buf,len,kcpref,user):
    global  kcp_LIB
    # c = kcp_LIB.ikcp_input(kcp, c_char_p(buf), len)
    # socket.send()
    return 0

# update 函数
def up_func(kcpVar):
    t = c_int()
    kcpref =byref(kcpVar)
    t.value = int(time.time()*1000)

    kcp_LIB.ikcp_update(kcpref,t)
    # wd = 'hello world'
    # buf = c_char_p(wd)
    # len = 11
    # # print("wsnd",kcp_LIB.ikcp_waitsnd(kcpref),kcpVar.snd_wnd)
    # if kcp_LIB.ikcp_waitsnd(kcpref) < 2*kcpVar.snd_wnd:
    #     b = kcp_LIB.ikcp_send(kcpref, buf, len)
    #     print('recv',b)
    # else:
    #     print("11111",kcp_LIB.ikcp_waitsnd(kcpref),kcpVar.snd_wnd,'value')
 


def log(buf,*arg):
    print(buf)
    pass


def test():
    global kcp_LIB
        
    # 加载库
    kcp_LIB = cdll.LoadLibrary('kcp_clib.so')

    # 创建kcp
    kcp_LIB.ikcp_create.restype = POINTER(ikcpcb)
    kcp_pointer = kcp_LIB.ikcp_create(12323, None)

    kcpVar = kcp_pointer.contents
    kcpref = byref(kcpVar)



    # 设置一系列配置
    kcpVar.logmask = c_int(0x0)
    kcpVar.rx_minrto  = 10
    kcp_LIB.ikcp_nodelay(kcpref, 1, 10, 2)
    kcp_LIB.ikcp_interval(kcpref,10)
    kcp_LIB.ikcp_wndsize.restype = c_int
    kcp_LIB.ikcp_wndsize.argtypes = [c_void_p,c_int,c_int]
    kcp_LIB.ikcp_setmtu.restype = c_int
    print("mtusetRes",kcp_LIB.ikcp_setmtu(byref(kcpVar),476))

    output1 =CFoutput(outputfunc)
    kcp_LIB.ikcp_setoutput(kcpref, output1)

    kcplog = CFlog(log)
    kcpVar.writelog =kcplog

    while(True):
        # 休眠 10 ms
        time.sleep(0.01)
        # 更新kcp update
        up_func(kcpVar)

if __name__ == '__main__':
    test()

 

    
   

   



