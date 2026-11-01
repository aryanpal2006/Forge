"use client";

import React, { useEffect } from 'react';
import dynamic from 'next/dynamic';

interface LeafletCommandMapProps {
  district: string;
  fleet: any[];
  orders: any[];
  activeHazardBbox?: number[] | null;
}

const CommandMapWrapper = dynamic(
  async () => {
    const { MapContainer, TileLayer, Marker, Popup, Polyline, Polygon, useMap } = await import('react-leaflet');
    const L = (await import('leaflet')).default;

    // Fix standard leaflet icon path issues in React
    delete (L.Icon.Default.prototype as any)._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    });

    const truckIcon = new L.Icon({
      iconUrl: 'https://cdn-icons-png.flaticon.com/512/2830/2830305.png',
      iconSize: [34, 34],
      iconAnchor: [17, 17],
      popupAnchor: [0, -17],
    });

    const MapRecenter = ({ center }: { center: [number, number] }) => {
      const map = useMap();
      useEffect(() => {
        map.setView(center, 10);
      }, [center]);
      return null;
    };

    return function DynamicCommandMap({ district, fleet, orders, activeHazardBbox }: LeafletCommandMapProps) {
      const centers: Record<string, [number, number]> = {
        solapur: [17.6599, 75.9064],
        darbhanga: [26.1542, 85.8918],
        cuddalore: [11.7480, 79.7714],
      };
      const center = centers[district.toLowerCase()] || [26.1542, 85.8918];

      // Extract route lines from orders
      const routeLines: { coords: [number, number][]; isRerouted: boolean; status: string }[] = [];
      orders.forEach((o) => {
        if (o.route_geojson?.geometry?.coordinates) {
          // GeoJSON is [lon, lat], Leaflet wants [lat, lon]
          const cList = o.route_geojson.geometry.coordinates.map((c: [number, number]) => [c[1], c[0]]);
          routeLines.push({
            coords: cList,
            isRerouted: o.rerouted_count > 0 || o.route_geojson.properties?.is_rerouted,
            status: o.status,
          });
        }
      });

      // Active hazard polygon coords if present
      let hazardPolygonCoords: [number, number][] = [];
      if (activeHazardBbox && activeHazardBbox.length === 4) {
        const [minLon, minLat, maxLon, maxLat] = activeHazardBbox;
        hazardPolygonCoords = [
          [minLat, minLon],
          [maxLat, minLon],
          [maxLat, maxLon],
          [minLat, maxLon],
        ];
      }

      return (
        <MapContainer
          center={center}
          zoom={10}
          scrollWheelZoom={false}
          className="w-full h-full rounded-2xl z-0"
          style={{ height: '540px', width: '100%' }}
        >
          <MapRecenter center={center} />
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Render Fleet Vehicles */}
          {fleet.map((veh) => (
            <Marker
              key={veh.id}
              position={[veh.current_lat, veh.current_lon]}
              icon={truckIcon}
            >
              <Popup>
                <div className="p-1 space-y-1 text-xs text-slate-900 font-sans">
                  <div className="font-extrabold text-blue-900 border-b pb-1">
                    {veh.vehicle_code} ({veh.vehicle_type})
                  </div>
                  <div>
                    <strong>Status:</strong>{' '}
                    <span className="uppercase font-bold text-emerald-600">{veh.status}</span>
                  </div>
                  <div>
                    <strong>Fuel Level:</strong> {veh.fuel_level_pct}%
                  </div>
                  <div>
                    <strong>Capacity:</strong> {veh.capacity_kg} kg
                  </div>
                  {veh.active_order_id && (
                    <div>
                      <strong>Order:</strong> {veh.active_order_id}
                    </div>
                  )}
                </div>
              </Popup>
            </Marker>
          ))}

          {/* Render Active Hazard Inundation Polygon */}
          {hazardPolygonCoords.length > 0 && (
            <Polygon
              positions={hazardPolygonCoords}
              pathOptions={{
                color: '#dc2626',
                fillColor: '#ef4444',
                fillOpacity: 0.6,
                weight: 2,
                dashArray: '6, 6',
              }}
            >
              <Popup>
                <div className="text-xs text-rose-800 font-bold p-1">
                  Active Hazard Barrier: Flood Inundation Polygon (Blocked Edges Avoided)
                </div>
              </Popup>
            </Polygon>
          )}

          {/* Render Safe & Rerouted Paths */}
          {routeLines.map((line, idx) => (
            <Polyline
              key={idx}
              positions={line.coords}
              pathOptions={{
                color: line.isRerouted ? '#10b981' : '#3b82f6',
                weight: 5,
                opacity: 0.85,
                dashArray: line.isRerouted ? '8, 8' : undefined,
              }}
            />
          ))}
        </MapContainer>
      );
    };
  },
  { ssr: false, loading: () => <div className="h-[540px] bg-slate-800 rounded-2xl flex items-center justify-center text-slate-400">Loading Command Map...</div> }
);

export const LeafletCommandMap: React.FC<LeafletCommandMapProps> = (props) => {
  return <CommandMapWrapper {...props} />;
};

