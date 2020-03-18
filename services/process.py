import sys
sys.path.append('.') # đoạn này để gọi import root folder của project vào module này : để gọi được đến các folder khác
import logging
# define top level module logger
logger = logging.getLogger(__name__)

def processdata():
    logger.warning("Đây là warning!")
    print("Đây là process:")
    logger.debug("Đây là debug!")
    logger.info("Đây là info!")
    logger.error("Đây là error!")
    logger.critical("Đây là critical")
    #logger.exception("Đây là exception")

def show():
    pass

# hiển thị biểu  đồ
# x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
# plt.plot(x, np.sin(x))       # Plot the sine of each x point
# plt.show()     
