#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: UHD WBFM Receive
# Author: Example
# Description: WBFM Receive
# Generated: Sat Apr 14 12:18:24 2018
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sip
import sys
import time
from gnuradio import qtgui


class wbfm_rx(gr.top_block, Qt.QWidget):

    def __init__(self, samp_rate=400e3, freq=91.2e6, gain=50):
        gr.top_block.__init__(self, "UHD WBFM Receive")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("UHD WBFM Receive")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "wbfm_rx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.samp_rate = samp_rate
        self.freq = freq
        self.gain = gain

        ##################################################
        # Variables
        ##################################################
        self.audio_decim = audio_decim = 10

        ##################################################
        # Blocks
        ##################################################
        self.volume = blocks.multiply_const_vcc((20, ))
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(('addr=192.168.10.3', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.qtgui_sink_x_0_0 = qtgui.sink_f(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_0_win)

        self.qtgui_sink_x_0_0.enable_rf_freq(False)



        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 200e3, 30e3, firdes.WIN_HANN, 6.76))
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_float*1, 'wfbm_rx2.log', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'wfbm_rx1.log', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.audio_sink = audio.sink(44100, "", True)
        self.analog_wfm_rcv = analog.wfm_rcv(
        	quad_rate=samp_rate,
        	audio_decimation=10,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv, 0), (self.audio_sink, 0))
        self.connect((self.analog_wfm_rcv, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.analog_wfm_rcv, 0), (self.qtgui_sink_x_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.volume, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.volume, 0), (self.analog_wfm_rcv, 0))
        self.connect((self.volume, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.volume, 0), (self.qtgui_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "wbfm_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.qtgui_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 200e3, 30e3, firdes.WIN_HANN, 6.76))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)


    def get_audio_decim(self):
        return self.audio_decim

    def set_audio_decim(self, audio_decim):
        self.audio_decim = audio_decim


def argument_parser():
    description = 'WBFM Receive'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "-s", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(400e3),
        help="Set Sample Rate [default=%default]")
    parser.add_option(
        "-s", "--freq", dest="freq", type="eng_float", default=eng_notation.num_to_str(91.2e6),
        help="Set freq_usrp [default=%default]")
    parser.add_option(
        "-s", "--gain", dest="gain", type="eng_float", default=eng_notation.num_to_str(50),
        help="Set Sample Rate [default=%default]")
    return parser


def main(top_block_cls=wbfm_rx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(samp_rate=options.samp_rate, freq=options.freq, gain=options.gain)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
