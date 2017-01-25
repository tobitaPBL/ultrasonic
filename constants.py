# Audio constants
RATE = 44100
CHUNK_SIZE = 512
AUDIOBUF_SIZE = 2048 #2048

# Constants for FSK
BASELINE = 17800.0

CHAR_FREQ = [18200.0, # end      -> over 1000
			 18400.0, # start    -> over
			 18600.0, # 0        -> over
			 18800.0, # 1        -> over
			 19000.0, # 2        -> over
			 19200.0, # 3        -> over
			 19400.0, # 4        -> over
			 19600.0, # 5        -> over
			 19800.0, # 6        -> over
			 20000.0] # 7        -> over

CHAR_THRESH = [1000, # end
			   1000, # start
			   1000, # 0
			   1000, # 1
			   1000, # 2
			   1000, # 3
			   1000, # 4
			   1000, # 5
			   1000, # 6
			   1000] # 7

BIT_DURATION = 0.05 # 0.1
IDLE_LIMIT = 10 # If we don't hear anything for a while (~2sec), clear buffer.
