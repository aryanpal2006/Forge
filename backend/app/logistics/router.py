import networkx as nx
import math
from typing import List, Dict, Any, Tuple, Optional

class DynamicRoadRouter:
    """Road network router using NetworkX with dynamic penalty routing to avoid hazard polygons."""

    def __init__(self):
        self.graphs: Dict[str, nx.Graph] = {}
        self.node_coords: Dict[str, Dict[str, Tuple[float, float]]] = {}
        self._build_road_graphs()

    def _build_road_graphs(self):
        # 1. Solapur Regional Road Network
        g_sol = nx.Graph()
        sol_nodes = {
            "Solapur_HQ": (17.6599, 75.9064),
            "Mohol_Junction": (17.8100, 75.6500),
            "Barshi_Hub": (18.2300, 76.0400),
            "Pandharpur_Crossing": (17.6700, 75.3200),
            "South_Solapur_Depot": (17.5200, 75.9800),
            "Madha_Turnoff": (18.0300, 75.5200),
            "Akkalkot_Gate": (17.5200, 76.2000)
        }
        self.node_coords["solapur"] = sol_nodes
        for n, coords in sol_nodes.items():
            g_sol.add_node(n, lat=coords[0], lon=coords[1])

        sol_edges = [
            ("Solapur_HQ", "Mohol_Junction", 32.0),
            ("Mohol_Junction", "Madha_Turnoff", 28.0),
            ("Solapur_HQ", "Barshi_Hub", 65.0),
            ("Barshi_Hub", "Madha_Turnoff", 42.0),
            ("Solapur_HQ", "Pandharpur_Crossing", 70.0),
            ("Mohol_Junction", "Pandharpur_Crossing", 45.0),
            ("Solapur_HQ", "South_Solapur_Depot", 20.0),
            ("South_Solapur_Depot", "Akkalkot_Gate", 35.0),
            ("Solapur_HQ", "Akkalkot_Gate", 38.0)
        ]
        for u, v, w in sol_edges:
            g_sol.add_edge(u, v, weight=w, base_distance_km=w, hazard_penalty=1.0)
        self.graphs["solapur"] = g_sol

        # 2. Darbhanga Regional Road Network (Flood Prone)
        g_dar = nx.Graph()
        dar_nodes = {
            "Darbhanga_Center": (26.1542, 85.8918),
            "Laheriasarai_Depot": (26.1150, 85.8950),
            "Kalyanpur_Village": (26.2200, 85.9400),
            "Keoti_Junction": (26.2800, 85.9100),
            "Baheri_Causeway": (26.0400, 86.0500),
            "Benipur_Crossing": (26.1200, 86.1200),
            "Hayaghat_Bridge": (26.0100, 85.8400),
            "Biraul_Spur": (26.0100, 86.2000)
        }
        self.node_coords["darbhanga"] = dar_nodes
        for n, coords in dar_nodes.items():
            g_dar.add_node(n, lat=coords[0], lon=coords[1])

        dar_edges = [
            ("Darbhanga_Center", "Laheriasarai_Depot", 6.0),
            ("Darbhanga_Center", "Kalyanpur_Village", 14.0),
            ("Kalyanpur_Village", "Keoti_Junction", 12.0),
            ("Darbhanga_Center", "Keoti_Junction", 20.0),
            ("Laheriasarai_Depot", "Hayaghat_Bridge", 18.0),
            ("Laheriasarai_Depot", "Baheri_Causeway", 24.0),
            ("Baheri_Causeway", "Benipur_Crossing", 15.0),
            ("Darbhanga_Center", "Benipur_Crossing", 28.0),
            ("Benipur_Crossing", "Biraul_Spur", 22.0)
        ]
        for u, v, w in dar_edges:
            g_dar.add_edge(u, v, weight=w, base_distance_km=w, hazard_penalty=1.0)
        self.graphs["darbhanga"] = g_dar

        # 3. Cuddalore Regional Road Network (Coastal)
        g_cud = nx.Graph()
        cud_nodes = {
            "Cuddalore_Port": (11.7480, 79.7714),
            "Panruti_Warehouse": (11.7700, 79.5500),
            "Kurinjipadi_Junction": (11.5700, 79.6000),
            "Chidambaram_Depot": (11.3900, 79.6900),
            "Nellikuppam_Crossing": (11.7700, 79.6800),
            "Vadalur_Hub": (11.5500, 79.5500)
        }
        self.node_coords["cuddalore"] = cud_nodes
        for n, coords in cud_nodes.items():
            g_cud.add_node(n, lat=coords[0], lon=coords[1])

        cud_edges = [
            ("Cuddalore_Port", "Nellikuppam_Crossing", 12.0),
            ("Nellikuppam_Crossing", "Panruti_Warehouse", 16.0),
            ("Cuddalore_Port", "Kurinjipadi_Junction", 26.0),
            ("Kurinjipadi_Junction", "Vadalur_Hub", 10.0),
            ("Panruti_Warehouse", "Vadalur_Hub", 24.0),
            ("Kurinjipadi_Junction", "Chidambaram_Depot", 22.0),
            ("Cuddalore_Port", "Chidambaram_Depot", 44.0)
        ]
        for u, v, w in cud_edges:
            g_cud.add_edge(u, v, weight=w, base_distance_km=w, hazard_penalty=1.0)
        self.graphs["cuddalore"] = g_cud

    def find_nearest_node(self, district_id: str, lat: float, lon: float) -> str:
        nodes = self.node_coords.get(district_id.lower(), self.node_coords["solapur"])
        best_node = None
        min_dist = float("inf")
        for node_name, (n_lat, n_lon) in nodes.items():
            d = (lat - n_lat)**2 + (lon - n_lon)**2
            if d < min_dist:
                min_dist = d
                best_node = node_name
        return best_node

    def compute_safe_route(
        self,
        district_id: str,
        origin_node: str,
        dest_node: str,
        hazard_polygons: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Computes shortest path avoiding or penalizing roads intersecting hazard polygons."""
        dist_norm = district_id.lower()
        if dist_norm not in self.graphs:
            dist_norm = "darbhanga"
            
        base_g = self.graphs[dist_norm]
        active_g = base_g.copy()
        
        penalized_edges = []
        blocked_edges = []

        # If hazard polygons provided (e.g. flood zone), detect intersecting edges
        if hazard_polygons:
            for poly in hazard_polygons:
                bbox = poly.get("bbox") # [min_lon, min_lat, max_lon, max_lat]
                severity = poly.get("severity", 0.9)
                if not bbox:
                    continue
                min_lon, min_lat, max_lon, max_lat = bbox
                
                # Check each edge
                for u, v in list(active_g.edges()):
                    u_lat, u_lon = active_g.nodes[u]["lat"], active_g.nodes[u]["lon"]
                    v_lat, v_lon = active_g.nodes[v]["lat"], active_g.nodes[v]["lon"]
                    
                    # Midpoint proxy check
                    mid_lat = (u_lat + v_lat) / 2.0
                    mid_lon = (u_lon + v_lon) / 2.0
                    
                    if (min_lat <= mid_lat <= max_lat) and (min_lon <= mid_lon <= max_lon):
                        if severity > 0.8: # Severely inundated -> sever edge
                            active_g.remove_edge(u, v)
                            blocked_edges.append((u, v))
                        else: # Partial hazard -> apply 10x penalty
                            curr_w = active_g[u][v]["weight"]
                            active_g[u][v]["weight"] = curr_w * 10.0
                            penalized_edges.append((u, v))

        # Check path existence
        try:
            path = nx.shortest_path(active_g, source=origin_node, target=dest_node, weight="weight")
            total_dist_km = sum(
                base_g[path[i]][path[i+1]]["base_distance_km"] for i in range(len(path) - 1)
            )
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            # If completely blocked, fallback to safest possible path on base graph with high penalty alert
            path = nx.shortest_path(base_g, source=origin_node, target=dest_node, weight="weight")
            total_dist_km = sum(
                base_g[path[i]][path[i+1]]["base_distance_km"] for i in range(len(path) - 1)
            )

        # Convert path to GeoJSON LineString coordinates
        coords = []
        for n in path:
            lat = base_g.nodes[n]["lat"]
            lon = base_g.nodes[n]["lon"]
            coords.append([lon, lat])

        geojson_route = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            },
            "properties": {
                "path_nodes": path,
                "total_distance_km": round(total_dist_km, 1),
                "estimated_transit_hours": round(total_dist_km / 35.0, 1), # avg 35 km/h in disaster conditions
                "is_rerouted": len(blocked_edges) > 0 or len(penalized_edges) > 0,
                "blocked_edges_avoided": len(blocked_edges)
            }
        }

        return {
            "route_geojson": geojson_route,
            "path_nodes": path,
            "distance_km": round(total_dist_km, 1),
            "is_rerouted": len(blocked_edges) > 0 or len(penalized_edges) > 0,
            "blocked_segments": blocked_edges
        }

road_router = DynamicRoadRouter()

