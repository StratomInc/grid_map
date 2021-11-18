import matplotlib.pyplot as plt
import _thread
from matplotlib.backend_bases import MouseButton
from matplotlib import colors
import numpy as np


import rclpy
from rclpy.node import Node

from grid_map_msgs.msg import GridMap


class ViewerManager(Node):
  def __init__(self):
    super().__init__('viewer_manager')

    self.declare_parameter('topic','/traversability_map')
    self.declare_parameter('layer','traversability')
 
    self.topic = self.get_parameter('topic').value
    self.layer = self.get_parameter('layer').value
    
    self.subscription = self.create_subscription( GridMap, self.topic, self.listener_callback, 10)
    self.subscription  # prevent unused variable warning
  
    self.fig, self.ax = plt.subplots()
  
    self.annotation = self.ax.annotate('',xy=(10, 10), xycoords='figure pixels')
    self.recieved_first = False
    self.ready = False
    self.data = np.random.rand(10,10)

  def listener_callback(self, msg):
    self.recieved_first = True
    index = msg.layers.index(self.layer) 
    self.data = np.asarray(msg.data[index].data).reshape(msg.data[index].layout.dim[0].size,msg.data[index].layout.dim[1].size)
    self.ready = True

  def on_click(self,event):
    x, y = event.x, event.y
    if event.inaxes:
      self.ax = event.inaxes  # the axes instance
      self.annotation.set(text=str(self.data[int(event.ydata+.5)][int(event.xdata+.5)]))
  

def main(args=None):
  rclpy.init(args=args)

  viewer_manager = ViewerManager()

  plt.title('Topic: '+viewer_manager.topic + '   Layer:'+viewer_manager.layer)
  plt.connect('button_press_event', viewer_manager.on_click)
 
  _thread.start_new_thread(rclpy.spin, (viewer_manager,))

  plt.ion() 
  while rclpy.ok():
    if viewer_manager.recieved_first:
      cmap = plt.get_cmap('Greys')
      cmap.set_bad(color='red')
      if viewer_manager.ready:
        viewer_manager.ax.imshow(viewer_manager.data, cmap=cmap, origin='lower')
        viewer_manager.ready=False
      plt.draw()
      plt.pause(0.01)
    
  viewer_manager.destroy_node()
  rclpy.shutdown()


if __name__ == '__main__':
  main()







