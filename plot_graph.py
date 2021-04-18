import folium
import argparse
from collections import namedtuple, defaultdict
import csv

Location=namedtuple("Location", ("lat", "lon"))
Point = namedtuple("Point", ("location", "size", "name"))
Path = namedtuple("Path", ("points", "width"))


def plot(output_path, 
         data_path, 
         lat_from, 
         lon_from, 
         lat_to,
         lon_to,
         size_from=None, 
         name_from=None, 
         size_to=None, 
         name_to=None,
         default_size=50000,
         default_edge_width=None,
         edge_width=None,
         default_edge_opacity=0.5,
         headers=None):

  data = []
  window = [90, -90, 180, -180]  # min_lat, max_lat, min_lon, max_lon

  with open(data_path) as i:
    if headers:
      reader = csv.DictReader(i, fieldnames=headers)
    else:
      reader = csv.DictReader(i)
    for l in reader:

      if size_from is not None:
        point_size_from=l[size_from]
      else:
        point_size_from=default_size

      if size_to is not None:
        point_size_to=l[size_to]
      else:
        point_size_to=default_size
      
      if name_from is not None:
        point_name_from=l[name_from]
      else:
        point_name_from=None

      if name_to is not None:
        point_name_to=l[name_to]
      else:
        point_name_to=None

      if edge_width is not None:
        width=l[edge_width]
      else:
        width=default_edge_width
 
      lat_from = float(l['lat_from'])
      lon_from = float(l['lon_from'])
      lat_to = float(l['lat_to'])
      lon_to = float(l['lon_to'])

      data.append(Path((
        Point(Location(lat_from, lon_from), point_size_from, point_name_from), 
        Point(Location(lat_to, lon_to), point_size_to, point_name_to)
      ), width))

      window[0] = min([window[0], lat_from, lat_to])
      window[1] = max([window[1], lat_from, lat_to])        
      window[2] = min([window[2], lon_from, lon_to])        
      window[3] = max([window[3], lon_from, lon_to])        
  my_map = folium.Map()
  my_map.fit_bounds(((window[1], window[2]),(window[0],window[3])))
  for path in data:
    for point in path.points:
      folium.Circle(location=point.location, 
                    radius=point.size,
                    fill=True,
                    fill_color='crimson', 
                    popup=point.name).add_to(my_map)
    folium.PolyLine([point.location for point in path.points], 
                    weight=path.width,
                    opacity=default_edge_opacity).add_to(my_map)

  my_map.save(output_path)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-o', '--output')
  parser.add_argument('-d', '--data')
  parser.add_argument('--lat-from', default='lat_from')
  parser.add_argument('--lon-from', default='lon_from')
  parser.add_argument('--lat-to', default='lat_to')
  parser.add_argument('--lon-to', default='lon_to')
  parser.add_argument('--size-from')
  parser.add_argument('--name-from')
  parser.add_argument('--size-to')
  parser.add_argument('--name-to')
  parser.add_argument('--default-size', default=50000)
  parser.add_argument('--default-edge_width', default=5)
  parser.add_argument('--edge-width')
  parser.add_argument('--default-edge-opacity', default=0.5)
  parser.add_argument('--headers', default=None)
  args = parser.parse_args()
  plot(args.output,
       args.data,
       args.lat_from,
       args.lon_from,
       args.lat_to,
       args.lon_to,
       args.size_from,
       args.name_from,
       args.size_to,
       args.name_to,
       args.default_size,
       args.default_edge_width,
       args.edge_width,
       args.default_edge_opacity,
       args.headers)


if __name__ == '__main__':
  main()
