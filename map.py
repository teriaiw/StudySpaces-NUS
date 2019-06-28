import folium

m = folium.Map(location =[1.295141, 103.773875], zoom_start = 20)

tooltip = 'this building'

folium.Marker([1.295141, 103.773875],
popup ='<strong> com1 </strong>',
tooltip = tooltip).add_to(m)

m.save('map.html')
