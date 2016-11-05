# Audio constants
RATE = 44100
CHUNK_SIZE = 512
AUDIOBUF_SIZE = 2048 #2048

# Constants for FSK
BASELINE = 17000.0

CHAR_FREQ = [17300.0, # end
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

CHAR_THRESH = [20, # end
			   20, # start
			   20, # 0
			   20, # 1
			   20, # 2
			   20, # 3
			   20, # 4
			   20, # 5
			   20, # 6
			   20, # 7
			   20, # 8
			   20, # 9
			   20, # 10
			   20, # 11
			   20, # 12
			   20, # 13
			   20, # 14
			   20] # 15

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

BIT_DURATION = 0.05 # 0.1
IDLE_LIMIT = 10 # If we don't hear anything for a while (~2sec), clear buffer.
