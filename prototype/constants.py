# Audio constants
RATE = 44100
CHUNK_SIZE = 256
AUDIOBUF_SIZE = 1024 #2048

# Constants for FSK
BASELINE = 17000.0

CHAR_FREQ = [17250.0, # end
			 17500.0, # start
			 17750.0, # 0
			 17900.0, # 1
			 18050.0, # 2
			 18200.0, # 3
			 18350.0, # 4
			 18500.0, # 5
			 18650.0, # 6
			 18800.0, # 7
			 18950.0, # 8
			 19100.0, # 9
			 19250.0, # 10
			 19400.0, # 11
			 19550.0, # 12
			 19700.0, # 13
			 19850.0, # 14
			 20000.0] # 15

CHAR_THRESH = [50, # end
			   50, # start
			   50, # 0
			   50, # 1
			   50, # 2
			   50, # 3
			   50, # 4
			   50, # 5
			   50, # 6
			   50, # 7
			   50, # 8
			   50, # 9
			   50, # 10
			   50, # 11
			   50, # 12
			   50, # 13
			   50, # 14
			   50] # 15

# CHARSTART = 17600.0
# CHARSTART_THRESH = 100

# ZERO = 18200.0
# ZERO_THRESH = 20

# ONE = 18800.0
# ONE_THRESH = 20

# TWO = 19400.0
# TWO_THRESH = 20

# THREE = 20000.0
# THREE_THRESH = 20

BIT_DURATION = 0.025 # 0.1
IDLE_LIMIT = 10 # If we don't hear anything for a while (~2sec), clear buffer.
