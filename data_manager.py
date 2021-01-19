import folium


def create_world_map():
    return folium.Map(location=[51.5098, 0], zoom_start=2.5, min_zoom=2.5)


def create_marker(location, popup, tooltip, map_object):
    """This function creates an instance of a marker"""
    folium.Marker(location=location, popup=f"Sighting {popup}", tooltip=tooltip).add_to(map_object)


world_map = create_world_map()
create_marker([42.363600, -71.099500], "1", "Click to learn more about this sighting", world_map)
create_marker([59.363600, -42.099500], "2", "Click to learn more about this sighting", world_map)

html_map = world_map._repr_html_()
