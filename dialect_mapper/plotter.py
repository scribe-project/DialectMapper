import json
import matplotlib as mpl
import matplotlib.colors as mpl_colors
import re
from shapely import Polygon, MultiPolygon

import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from . import mapping_data

class ColorMap():
    '''
    This class is copied/borrowed from the geoplotlib package
    '''
    def __init__(self, cmap_name, levels=10):
        """
        Converts continuous values into colors using matplotlib colorscales
        :param cmap_name: colormap name
        :param levels: discretize the colorscale into levels
        """
        self.cmap = mpl.colormaps[cmap_name]
        self.levels = levels

    def to_color_linear_scale(self, value, maxvalue, minvalue=0.0):
        """
        convert continuous values into colors using matplotlib colorscales
        :param value: value to be converted
        :param maxvalue: max value in the colorscale
        :param minvalue: minimum of the input values in linear scale (default is 0)
        :return: the color corresponding to the value
        """
        if minvalue >= maxvalue:
            raise Exception('minvalue must be less than maxvalue')
        else:
            value = 1.*(value-minvalue) / (maxvalue-minvalue)

        if value < 0:
            value = 0
        elif value > 1:
            value = 1

        value = int(1.*self.levels*value)*1./(self.levels-1)
        value = self.cmap(value)
        return mpl_colors.to_hex(value)



class plotter_methods:

    def _create_poly(self, obj):
        if len(obj) > 1:
            return Polygon(obj[0], holes=obj[1:])
        else:
            return Polygon(obj[0])

    def _process_features(self, features, get_color):
        svg_list = []
        min_x = None
        min_y = None
        max_x = None
        max_y = None
        for region_features in features:
            region_multiPolygon = MultiPolygon(
                [self._create_poly(obj) for obj in region_features['geometry']['coordinates']]
            )
            svg_list.append(
                self.stroke_width_pat.sub(
                    'stroke-width="0.025"',
                    region_multiPolygon.svg(fill_color=get_color(region_features['properties']['navn']), opacity=1)
                )   
            )
            mp_bounds = region_multiPolygon.bounds
            if min_x == None:
                min_x = mp_bounds[0]
            if min_y == None:
                min_y = mp_bounds[1]
            if max_x == None:
                max_x = mp_bounds[2]
            if max_y == None:
                max_y = mp_bounds[3]
            
            if mp_bounds[0] < min_x:
                min_x = mp_bounds[0]
            if mp_bounds[1] < min_y:
                min_y = mp_bounds[1]
            if mp_bounds[2] > max_x:
                max_x = mp_bounds[2]
            if mp_bounds[3] > max_y:
                max_y = mp_bounds[3]

        width = max_x - min_x
        height = max_y - min_y
        return svg_list, min_x, min_y, width, height

    def plot_kommune_regions(
        self, 
        output_svg_filepath, 
        kommune_region_to_value={}, 
        color_map_name='Blues', 
        color_map_levels=50, 
        max_region_value=30, 
        default_color='#66cc99', 
        final_width='500', 
        final_height='500'):

        cmap = ColorMap(color_map_name, levels=color_map_levels)
        def get_color(dialect_name):
            if dialect_name in kommune_region_to_value:
                return cmap.to_color_linear_scale(kommune_region_to_value.get(dialect_name), max_region_value)
            else:
                return default_color
        svg_list, min_x, min_y, width, height = self._process_features(self.kommuner_json['features'], get_color)
        with open(output_svg_filepath, 'w') as open_f:
            open_f.write(
                self.head_bit.format(
                    str(float(final_width)),
                    str(float(final_height)),
                    min_x, 
                    min_y, 
                    width, 
                    height ) + 
                ''.join(svg_list) + 
                self.end_bit
            )

    def plot_dialect_regions(
        self, 
        output_svg_filepath, 
        dialect_region_to_value={}, 
        color_map_name='Blues', 
        color_map_levels=50, 
        max_region_value=30, 
        default_color='#66cc99', 
        final_width='500', 
        final_height='500'):

        cmap = ColorMap(color_map_name, levels=color_map_levels)
        def get_color(dialect_name):
            if dialect_name in dialect_region_to_value:
                return cmap.to_color_linear_scale(dialect_region_to_value.get(dialect_name), max_region_value)
            else:
                return default_color

        svg_list, min_x, min_y, width, height = self._process_features(self.dialekter_json['features'], get_color)
        with open(output_svg_filepath, 'w') as open_f:
            open_f.write(
                self.head_bit.format(
                    str(float(final_width)),
                    str(float(final_height)),
                    min_x, 
                    min_y, 
                    width, 
                    height ) + 
                ''.join(svg_list) + 
                self.end_bit
            )
        
    def __init__(self) -> None:
        self.dialekter_json = json.load(
            StringIO(
                pkg_resources.read_text(
                    mapping_data, 
                    'dialekter_geojson.json'
                )
            )
        )
        self.kommuner_json = json.load(
            StringIO(
                pkg_resources.read_text(
                    mapping_data, 
                    'kommuner_komprimert.json'
                )
            )
        )
        self.stroke_width_pat = re.compile('stroke-width=".*?"')
        self.head_bit = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{}" height="{}" viewBox="{} {} {} {}" preserveAspectRatio="xMinYMin meet"><g transform="matrix(1,0,0,-1,0,139.540897)">'''
        self.end_bit = '''</g></svg>'''
