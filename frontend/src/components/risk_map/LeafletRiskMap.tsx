"use client";

import React, { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

interface LeafletRiskMapProps {
  district: string;
  gridData: any;
  activeLayer: 'drought' | 'flood' | 'heat' | 'ndvi';
  horizonDays: number;
}

// Dynamically import MapContainer and related Leaflet components to avoid SSR window errors
const MapWrapper = dynamic(
  async () => {
    const { MapContainer, TileLayer, Polygon, Popup, Tooltip, useMap } = await import('react-leaflet');
    const L = (await import('leaflet')).default;

    // Component to center map on district bounds
    const MapRecenter = ({ center }: { center: [number, number] }) => {
      const map = useMap();
      useEffect(() => {
        map.setView(center, 10);
      }, [center]);
      return null;
    };

    return function DynamicMap({ district, gridData, activeLayer, horizonDays }: LeafletRiskMapProps) {
      const centers: Record<string, [number, number]> = {
        solapur: [17.6599, 75.9064],
        darbhanga: [26.1542, 85.8918],
        cuddalore: [11.7480, 79.7714],
      };
      const center = centers[district.toLowerCase()] || [17.6599, 75.9064];

      // Helper to compute fill color based on active layer value
      const getColor = (val: number, layer: string) => {
        if (layer === 'drought') {
          // Orange gradient
          return val > 0.7 ? '#ea580c' : val > 0.4 ? '#f97316' : val > 0.2 ? '#fbbf24' : '#fef08a';
        } else if (layer === 'flood') {
          // Blue gradient
          return val > 0.7 ? '#1d4ed8' : val > 0.4 ? '#3b82f6' : val > 0.2 ? '#60a5fa' : '#bfdbfe';
        } else if (layer === 'heat') {
          // Red gradient
          return val > 0.7 ? '#b91c1c' : val > 0.4 ? '#ef4444' : val > 0.2 ? '#f87171' : '#fecaca';
        } else {
          // NDVI: Green/Brown
          return val > 0.6 ? '#78350f' : val > 0.4 ? '#d97706' : '#15803d';
        }
      };

      const features = gridData?.features || [];

      return (
        <MapContainer
          center={center}
          zoom={10}
          scrollWheelZoom={false}
          className="w-full h-full rounded-2xl z-0"
          style={{ height: '520px', width: '100%' }}
        >
          <MapRecenter center={center} />
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {features.map((feat: any, idx: number) => {
            const props = feat.properties || {};
            // Coordinates in GeoJSON are [lon, lat], Leaflet Polygon expects [lat, lon]
            const coords = feat.geometry?.coordinates?.[0] || [];
            const latLngs = coords.map((c: [number, number]) => [c[1], c[0]]);

            let metricVal = props.drought_risk;
            let metricName = "Drought Probability";
            if (activeLayer === 'flood') {
              metricVal = props.flood_risk;
              metricName = "Flash-Flood Risk";
            } else if (activeLayer === 'heat') {
              metricVal = props.heat_stress;
              metricName = "Heatwave Stress";
            } else if (activeLayer === 'ndvi') {
              metricVal = props.ndvi_stress;
              metricName = "NDVI Vegetation Stress";
            }

            // Adjust by horizon days multiplier for visual simulation
            const adjustedVal = Math.min(1.0, Math.max(0.0, metricVal * (1.0 + (horizonDays - 7) * 0.03)));
            const fillColor = getColor(adjustedVal, activeLayer);

            return (
              <Polygon
                key={props.cell_code || idx}
                positions={latLngs}
                pathOptions={{
                  fillColor: fillColor,
                  fillOpacity: 0.55,
                  weight: 1.2,
                  color: '#ffffff',
                  opacity: 0.8,
                }}
              >
                <Popup>
                  <div className="p-1 space-y-1 text-slate-900 text-xs font-sans">
                    <div className="font-bold border-b pb-1 text-emerald-800">
                      Grid Cell: {props.cell_code}
                    </div>
                    <div>
                      <strong>{metricName}:</strong> {(adjustedVal * 100).toFixed(1)}%
                    </div>
                    <div>
                      <strong>Yield Impact Deviation:</strong> {props.yield_deviation_pct}%
                    </div>
                    <div>
                      <strong>90% Uncertainty Band:</strong> [{props.uncertainty_lower}%, {props.uncertainty_upper}%]
                    </div>
                    <div>
                      <strong>Dominant Driver:</strong> {props.dominant_driver}
                    </div>
                    <div>
                      <strong>NDVI Vegetation Mean:</strong> {props.ndvi_mean}
                    </div>
                  </div>
                </Popup>
                <Tooltip direction="top" opacity={0.9}>
                  <span className="font-bold text-xs">
                    {props.cell_code}: {(adjustedVal * 100).toFixed(0)}%
                  </span>
                </Tooltip>
              </Polygon>
            );
          })}
        </MapContainer>
      );
    };
  },
  { ssr: false, loading: () => <div className="h-[520px] bg-slate-800 rounded-2xl flex items-center justify-center text-slate-400">Loading Leaflet Map Engine...</div> }
);

export const LeafletRiskMap: React.FC<LeafletRiskMapProps> = (props) => {
  return <MapWrapper {...props} />;
};

