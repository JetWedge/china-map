import folium
import webbrowser
import os

# Define the cities and their attractions with descriptions
cities_data = {
    "Beijing": {
        "coordinates": [39.9042, 116.4074],
        "attractions": [
            {"name": "Forbidden City", "coordinates": [39.9163, 116.3972], "description": "Imperial palace complex with rich history"},
            {"name": "Great Wall (Jinshanling)", "coordinates": [40.6500, 117.2333], "description": "Scenic, less crowded wall section"},
            {"name": "Summer Palace", "coordinates": [39.9999, 116.2750], "description": "Serene lakeside royal garden"},
            {"name": "Temple of Heaven", "coordinates": [39.8822, 116.4066], "description": "Historic site for imperial ceremonies"},
            {"name": "Hutongs", "coordinates": [39.9400, 116.4000], "description": "Traditional alleys showcasing local life"}
        ]
    },
    "Shanghai": {
        "coordinates": [31.2304, 121.4737],
        "attractions": [
            {"name": "The Bund", "coordinates": [31.2337, 121.4903], "description": "Historic waterfront with colonial architecture"},
            {"name": "Yu Garden", "coordinates": [31.2271, 121.4748], "description": "Classical Chinese garden oasis"},
            {"name": "Zhujiajiao Water Town", "coordinates": [31.1116, 121.0562], "description": "Ancient canals and bridges"},
            {"name": "Shanghai Museum", "coordinates": [31.2289, 121.4733], "description": "Extensive collection of Chinese art"},
            {"name": "Longhua Temple", "coordinates": [31.1725, 121.4450], "description": "Oldest temple in Shanghai"}
        ]
    },
    "Xi'an": {
        "coordinates": [34.3416, 108.9398],
        "attractions": [
            {"name": "Terracotta Warriors", "coordinates": [34.3843, 109.2789], "description": "Thousands of life-sized ancient soldiers"},
            {"name": "City Wall", "coordinates": [34.2920, 108.9465], "description": "Well-preserved ancient fortifications"},
            {"name": "Big Wild Goose Pagoda", "coordinates": [34.2197, 108.9597], "description": "Iconic Buddhist pagoda"},
            {"name": "Muslim Quarter", "coordinates": [34.2647, 108.9408], "description": "Vibrant street food and culture"},
            {"name": "Shaanxi History Museum", "coordinates": [34.2197 - 0.02, 108.9597], "description": "Artifacts from ancient dynasties"}
        ]
    },
    "Chengdu": {
        "coordinates": [30.5728, 104.0668],
        "attractions": [
            {"name": "Giant Panda Base", "coordinates": [30.7333, 104.1500], "description": "Conservation center for pandas"},
            {"name": "Wuhou Shrine", "coordinates": [30.6500, 104.0500], "description": "Memorial to strategist Zhuge Liang"},
            {"name": "Jinli Street", "coordinates": [30.6500 - 0.02, 104.0500], "description": "Traditional architecture and snacks"},
            {"name": "Mount Qingcheng", "coordinates": [30.9000, 103.5000], "description": "Taoist mountain with lush scenery"},
            {"name": "Dujiangyan Irrigation", "coordinates": [30.9989, 103.6189], "description": "Ancient engineering marvel"}
        ]
    },
    "Guilin": {
        "coordinates": [25.2744, 110.2903],
        "attractions": [
            {"name": "Li River Cruise", "coordinates": [25.2744, 110.2903 + 0.02], "description": "Scenic karst landscapes along river"},
            {"name": "Reed Flute Cave", "coordinates": [25.2833, 110.2833], "description": "Illuminated limestone formations"},
            {"name": "Elephant Trunk Hill", "coordinates": [25.2833 - 0.02, 110.2833], "description": "Iconic rock resembling elephant"},
            {"name": "Longji Rice Terraces", "coordinates": [25.7500, 110.1500], "description": "Layered fields on hillsides"},
            {"name": "Seven Star Park", "coordinates": [25.2833 + .02, 110.2833], "description": "Natural park with caves and zoo"}
        ]
    },
    "Lijiang": {
        "coordinates": [26.8721, 100.2299],
        "attractions": [
            {"name": "Old Town", "coordinates": [26.8721 + 0.02, 100.2299], "description": "UNESCO site with Naxi culture"},
            {"name": "Black Dragon Pool", "coordinates": [26.8721 - 0.02, 100.2299], "description": "Park with stunning views"},
            {"name": "Jade Dragon Snow Mountain", "coordinates": [27.1000, 100.2000], "description": "Snowy peaks and glaciers"},
            {"name": "Baisha Village", "coordinates": [26.9500, 100.2000], "description": "Ancient murals and local life"},
            {"name": "Shuhe Ancient Town", "coordinates": [26.9000, 100.2000], "description": "Tranquil traditional village"}
        ]
    },
    "Hangzhou": {
        "coordinates": [30.2741, 120.1551],
        "attractions": [
            {"name": "West Lake", "coordinates": [30.2500, 120.1500], "description": "Scenic lake with pagodas and bridges"},
            {"name": "Lingyin Temple", "coordinates": [30.2500 - 0.02, 120.1500], "description": "Historic Buddhist site in forest"},
            {"name": "Tea Plantations", "coordinates": [30.2500 + 0.02, 120.1500], "description": "Experience traditional tea culture"},
            {"name": "Six Harmonies Pagoda", "coordinates": [30.2000, 120.1500], "description": "Ancient riverside pagoda"},
            {"name": "Xixi Wetlands", "coordinates": [30.2500, 120.0500], "description": "Urban wetland with rich biodiversity"}
        ]
    },
    "Suzhou": {
        "coordinates": [31.2990, 120.5853],
        "attractions": [
            {"name": "Humble Administrator's Garden", "coordinates": [31.3167, 120.6333], "description": "Classic Chinese garden design"},
            {"name": "Tiger Hill", "coordinates": [31.3333, 120.5833], "description": "Historic site with leaning pagoda"},
            {"name": "Shantang Street", "coordinates": [31.3167 - 0.02, 120.5833], "description": "Ancient street along canal"},
            {"name": "Suzhou Silk Museum", "coordinates": [31.3167, 120.6333 - 0.02], "description": "History of silk production"},
            {"name": "Master of Nets Garden", "coordinates": [31.3000, 120.6333], "description": "Small yet exquisite garden"}
        ]
    },
    "Zhangjiajie": {
        "coordinates": [29.3274, 110.4342],
        "attractions": [
            {"name": "Avatar Mountains", "coordinates": [29.3274, 110.4342 - 0.02], "description": "Pillar-like formations in park"},
            {"name": "Glass Bridge", "coordinates": [29.3274 - 0.02, 110.4342], "description": "Longest glass-bottom bridge worldwide"},
            {"name": "Tianmen Mountain", "coordinates": [29.0500, 110.4833], "description": "Cliff-hanging walkways and views"},
            {"name": "Baofeng Lake", "coordinates": [29.3274 + 0.02, 110.4342], "description": "Boat rides among peaks"},
            {"name": "Golden Whip Stream", "coordinates": [29.3274, 110.4342 + 0.02], "description": "Scenic forest hiking trail"}
        ]
    },
    "Huangshan": {
        "coordinates": [30.1299, 118.1694],
        "attractions": [
            {"name": "Yellow Mountains", "coordinates": [30.1299, 118.1694 + 0.02], "description": "Granite peaks and pine trees"},
            {"name": "Sea of Clouds", "coordinates": [30.1299 - 0.02, 118.1694], "description": "Misty vistas from summits"},
            {"name": "Hot Springs", "coordinates": [30.1299 + 0.02, 118.1694], "description": "Natural pools near base"},
            {"name": "Hongcun Village", "coordinates": [30.0000, 118.0000], "description": "Ancient village with canals"},
            {"name": "Xidi Village", "coordinates": [30.0000 - 0.02, 118.0000], "description": "UNESCO village with old charm"}
        ]
    },
    "Dali": {
        "coordinates": [25.6065, 100.2676],
        "attractions": [
            {"name": "Erhai Lake", "coordinates": [25.6065+0.02, 100.2676], "description": "Scenic freshwater lake with bike routes"},
            {"name": "Three Pagodas", "coordinates": [25.7000, 100.2000], "description": "Iconic Buddhist pagoda trio"},
            {"name": "Dali Ancient Town", "coordinates": [25.6065 - 0.02, 100.2676], "description": "Stone streets and Bai culture"},
            {"name": "Cangshan Mountain", "coordinates": [25.7000 - 0.02, 100.2000], "description": "Trails and cable car views"},
            {"name": "Chongsheng Temple", "coordinates": [25.7000 + 0.02, 100.2000], "description": "Historic temple by the lake"}
        ]
    },
    "Kunming": {
        "coordinates": [24.8801, 102.8329],
        "attractions": [
            {"name": "Stone Forest", "coordinates": [24.8801 + 0.02, 102.8329], "description": "Karst limestone formations"},
            {"name": "Dian Lake", "coordinates": [24.8801 - 0.02, 102.8329], "description": "Yunnan's largest freshwater lake"},
            {"name": "Yuantong Temple", "coordinates": [25.0500, 102.7000], "description": "One of Yunnan's oldest temples"},
            {"name": "Green Lake Park", "coordinates": [25.0500 - 0.02, 102.7000], "description": "Urban park with teahouses"},
            {"name": "Golden Temple", "coordinates": [25.0500 + 0.02, 102.7000], "description": "Bronze temple in scenic park"}
        ]
    },
    "Nanjing": {
        "coordinates": [32.0603, 118.7969],
        "attractions": [
            {"name": "Sun Yat-sen Mausoleum", "coordinates": [32.0603 + 0.02, 118.7969], "description": "Tribute to revolutionary leader"},
            {"name": "Nanjing Massacre Museum", "coordinates": [32.0500, 118.7500], "description": "WWII history memorial"},
            {"name": "Confucius Temple", "coordinates": [32.0333, 118.7833], "description": "Cultural center with shops"},
            {"name": "Xuanwu Lake", "coordinates": [32.0833, 118.8000], "description": "Urban lake with island gardens"},
            {"name": "Ming Xiaoling Mausoleum", "coordinates": [32.0500, 118.8500], "description": "Tomb of Ming emperor"}
        ]
    }
}

def create_china_map():
    """Create a Folium map of China with cities and attractions."""
    # Center the map on China
    china_center = [35.8617, 104.1954]
    m = folium.Map(
        location=china_center,
        zoom_start=5,
        tiles='cartodbdark_matter'
    )
    
    # Process cities first to ensure they're on top
    for city_name, city_data in cities_data.items():
        # Add city marker with permanent tooltip
        folium.CircleMarker(
            location=city_data["coordinates"],
            radius=15,
            color="red",
            fill=True,
            weight=2,
            tooltip=folium.Tooltip(
                text=city_name,
                permanent=True,
                direction='right',
                sticky=False,
                style="""
                    font-size: 14px;
                    font-weight: bold;
                    color: black;
                    background-color: white;
                    border: none;
                    box-shadow: none;
                    padding: 1px 2px;
                    border-radius: 3px;
                """
            )
        ).add_to(m)
        
        # Add attractions as smaller blue circles with labels
        for attraction in city_data["attractions"]:
            # Add attraction marker
            folium.CircleMarker(
                location=attraction["coordinates"],
                radius=8,
                color="blue",
                fill=True,
                weight=1
            ).add_to(m)
            
            # Add clickable label with popup
            folium.Marker(
                location=attraction["coordinates"],
                icon=folium.DivIcon(
                    html=f'''
                        <div style="
                            font-size: 12px;
                            color: white;
                            background-color: transparent;
                            padding: 3px 6px;
                            cursor: pointer;
                            white-space: nowrap;
                            position: absolute;
                            transform: translate(15px, -10px);
                        ">{attraction["name"]}</div>
                    '''
                ),
                popup=folium.Popup(
                    html=f'<div style="font-size: 12px; padding: 5px; min-width: 150px;">{attraction["description"]}</div>',
                    max_width=300
                )
            ).add_to(m)
    
    # Save the map
    map_path = "china_top_cities.html"
    m.save(map_path)
    
    # Get the absolute path to the HTML file
    abs_path = os.path.abspath(map_path)
    
    # Open the map in a web browser
    webbrowser.open(f"file://{abs_path}")
    
    print(f"Map saved to: {abs_path}")
    print("You can share this file with others to view the map.")

if __name__ == "__main__":
    create_china_map()