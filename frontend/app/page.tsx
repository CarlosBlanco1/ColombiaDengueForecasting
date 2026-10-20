import { DengueMap } from "./components/DengueMap";
import { ForecastRange } from "./components/ForecastRange";
import { ForecastWeekSelect } from "./components/ForecastWeekSelect";
import { MapPinIcon } from "./components/icons/MapPinIcon";
import { PredictedCasesCard } from "./components/PredictedCasesCard";

export default function Home() {
  return (
    <div className="grid grid-rows-13 grid-cols-5 h-full">
      <div className="row-span-1 col-span-5 flex items-center">
        <div className="col-span-5 grid grid-cols-4 gap-3 p-4">
          <ForecastWeekSelect></ForecastWeekSelect>
          <div className="col-span-3 border-l-2 border-gray-300 flex items-center justify-start gap-3 pl-3">
            <MapPinIcon width={24} height={24} color="#003636"></MapPinIcon>
            <span className="text-xl">32 departments</span>
          </div>
        </div>
      </div>
      <div className="row-span-12 col-span-5 grid grid-cols-3 grid-rows-1 gap-3 p-4">
        <div className="row-span-1 col-span-2 grid grid-cols-1 grid-rows-1 border border-gray-300 rounded-xl">
          <DengueMap></DengueMap>
        </div>
        <div className="row-span-1 col-span-1 grid grid-rows-9 p-4 gap-3 border border-gray-300 rounded-xl bg-[#FDFCFB]">
          <div className="row-span-1 flex flex-col gap-1">
            <span className="text-black text-3xl font-semibold">Select a department</span>
            <span className="text-gray-500 text-2xl">Click a department on the map to view its forecast.</span>
          </div>
          <div className="row-span-5">
            <PredictedCasesCard></PredictedCasesCard>
          </div>
          <div className="row-span-3">
            <ForecastRange></ForecastRange>
          </div>
        </div>
      </div>
    </div>
  );
}
