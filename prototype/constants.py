# Audio constants
RATE = 44100
CHUNK_SIZE = 512
AUDIOBUF_SIZE = 2048 #2048

# Constants for FSK
BASELINE = 17500.0

CHAR_FREQ = [17750.0, # 0        -> over
			 18000.0, # 1        -> over
			 18250.0, # 2        -> over
			 18500.0, # 3        -> over
			 18750.0, # 4        -> over
			 19000.0, # 5        -> over
			 19250.0, # 6        -> over
			 19500.0] # 7        -> over

CHAR_THRESH = [700, # 0
			   700, # 1
			   700, # 2
			   700, # 3
			   700, # 4
			   700, # 5
			   200, # 6
			   50] # 7

BIT_DURATION = 0.05 # 0.1
IDLE_LIMIT = 5 # If we don't hear anything for a while (~2sec), clear buffer.
