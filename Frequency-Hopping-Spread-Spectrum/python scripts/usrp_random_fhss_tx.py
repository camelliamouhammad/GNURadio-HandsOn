#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Frequency Hopping Spread Spectrum (FHSS) Random Sequence
# Author: astro
# Description: This is a demonstartion of FHSS Based on FHSS OOT block for sequence generator
# Generated: Sat Jan 27 18:23:54 2018
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import Spread
import os
import pmt
import random
import sip
import sys
import time


class usrp_random_fhss_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Frequency Hopping Spread Spectrum (FHSS) Random Sequence")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Frequency Hopping Spread Spectrum (FHSS) Random Sequence")
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

        self.settings = Qt.QSettings("GNU Radio", "usrp_random_fhss_tx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.interp = interp = 10
        
        self.tx_taps = tx_taps = firdes.low_pass(1.0, samp_rate*interp, 20e3, 10e3, firdes.WIN_BLACKMAN, 6.76)
          
        self.seed = seed = 1
        self.nCH = nCH = 40
        self.gain = gain = 30
        self.freq = freq = 2.41e9
        self.ch_spacing = ch_spacing = 10000

        ##################################################
        # Blocks
        ##################################################
        self.tab = Qt.QTabWidget()
        self.tab_widget_0 = Qt.QWidget()
        self.tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0)
        self.tab_grid_layout_0 = Qt.QGridLayout()
        self.tab_layout_0.addLayout(self.tab_grid_layout_0)
        self.tab.addTab(self.tab_widget_0, "FFT")
        self.tab_widget_1 = Qt.QWidget()
        self.tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_1)
        self.tab_grid_layout_1 = Qt.QGridLayout()
        self.tab_layout_1.addLayout(self.tab_grid_layout_1)
        self.tab.addTab(self.tab_widget_1, "Waterfall")
        self.top_layout.addWidget(self.tab)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (tx_taps), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.fft = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.fft.set_update_time(0.10)
        self.fft.set_y_axis(-140, 10)
        self.fft.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.fft.enable_autoscale(False)
        self.fft.enable_grid(False)
        self.fft.set_fft_average(1.0)
        self.fft.enable_control_panel(False)
        
        if not True:
          self.fft.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.fft.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.fft.set_line_label(i, "Data {0}".format(i))
            else:
                self.fft.set_line_label(i, labels[i])
            self.fft.set_line_width(i, widths[i])
            self.fft.set_line_color(i, colors[i])
            self.fft.set_line_alpha(i, alphas[i])
        
        self._fft_win = sip.wrapinstance(self.fft.pyqwidget(), Qt.QWidget)
        self.tab_layout_0.addWidget(self._fft_win)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("trig"), 100)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate*interp, analog.GR_COS_WAVE, freq, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 150, 1, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=interp*samp_rate,
        	tau=75e-6,
        	max_dev=5e3,
                )
        self.Waterfall = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
                1 #number of inputs
        )
        self.Waterfall.set_update_time(0.10)
        self.Waterfall.enable_grid(False)
        
        if not True:
          self.Waterfall.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.Waterfall.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.Waterfall.set_line_label(i, "Data {0}".format(i))
            else:
                self.Waterfall.set_line_label(i, labels[i])
            self.Waterfall.set_color_map(i, colors[i])
            self.Waterfall.set_line_alpha(i, alphas[i])
        
        self.Waterfall.set_intensity_range(-140, 10)
        
        self._Waterfall_win = sip.wrapinstance(self.Waterfall.pyqwidget(), Qt.QWidget)
        self.tab_layout_1.addWidget(self._Waterfall_win)
        self.Spread_fhss_sequence_generator_0_0 = Spread.fhss_sequence_generator(seed, ch_spacing, nCH)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.Spread_fhss_sequence_generator_0_0, 'seq'), (self.analog_sig_source_x_0_0, 'freq'))    
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.Spread_fhss_sequence_generator_0_0, 'trig'))    
        self.connect((self.analog_nbfm_tx_0, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.analog_nbfm_tx_0, 0))    
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.Waterfall, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.fft, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 1))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "usrp_random_fhss_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def setStyleSheetFromFile(self, filename):
        try:
            if not os.path.exists(filename):
                filename = os.path.join(
                    gr.prefix(), "share", "gnuradio", "themes", filename)
            with open(filename) as ss:
                self.setStyleSheet(ss.read())
        except Exception as e:
            print >> sys.stderr, e

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.Waterfall.set_frequency_range(0, self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate*self.interp)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.fft.set_frequency_range(0, self.samp_rate)

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate*self.interp)

    def get_tx_taps(self):
        return self.tx_taps

    def set_tx_taps(self, tx_taps):
        self.tx_taps = tx_taps
        self.fft_filter_xxx_0.set_taps((self.tx_taps))

    def get_seed(self):
        return self.seed

    def set_seed(self, seed):
        self.seed = seed

    def get_nCH(self):
        return self.nCH

    def set_nCH(self, nCH):
        self.nCH = nCH

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0.set_gain(self.gain, 0)
        	

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.analog_sig_source_x_0_0.set_frequency(self.freq)
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)

    def get_ch_spacing(self):
        return self.ch_spacing

    def set_ch_spacing(self, ch_spacing):
        self.ch_spacing = ch_spacing


def main(top_block_cls=usrp_random_fhss_tx, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.setStyleSheetFromFile('/usr/share/gnuradio/themes/projector.qss')
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
