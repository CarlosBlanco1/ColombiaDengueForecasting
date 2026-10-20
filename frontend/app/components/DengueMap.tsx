"use client";

import { Dispatch, SetStateAction } from "react";
import {
    ComposableMap,
    Geographies,
    Geography,
    ZoomableGroup,
} from "react-simple-maps";

export function DengueMap({ selectedCode, setSelectedCode, geoUrl }:
    {
        selectedCode: string | null;
        setSelectedCode: Dispatch<SetStateAction<string | null>>;
        geoUrl: string
    }) {

    return <>
        <div className="border row-span-1 col-span-1 rounded-xl border-gray-100 max-h-full">
            <ComposableMap
                projection="geoMercator"
                projectionConfig={{ center: [-73.5, 4.5], scale: 2000 }}
            >
                <ZoomableGroup center={[-73.5, 4.5]}
                    zoom={1}
                    maxZoom={12}
                    translateExtent={[
                        [0, 0],
                        [800, 600],
                    ]}>

                    <Geographies geography={geoUrl}>
                        {({ geographies }) =>
                            geographies.map((geo) => {
                                const code = String(geo.properties!.dpto_ccdgo).padStart(2, "0");
                                const selected = code === selectedCode;

                                return (
                                    <Geography
                                        width={800}
                                        height={600}
                                        key={geo.rsmKey}
                                        geography={geo}
                                        fill={selected ? "#007B66" : "#C2E2CE"}
                                        stroke="#FFFFFF"
                                        strokeWidth={0.8}
                                        onClick={() => setSelectedCode(code)}
                                        style={{ outline: "none", cursor: "pointer" }}
                                    />
                                );
                            })
                        }
                    </Geographies>
                </ZoomableGroup>

            </ComposableMap>
        </div>
    </>
}