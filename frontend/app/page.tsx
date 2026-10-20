import { DengueMap } from "./components/DengueMap";
import { ForecastRange } from "./components/ForecastRange";
import { ForecastWeekSelect } from "./components/ForecastWeekSelect";
import { PeopleIcon } from "./components/icons/PeopleIcon";
import { PredictedCasesCard } from "./components/PredictedCasesCard";

export default function Home() {
  return (
    <div className="grid grid-rows-13 grid-cols-5 h-full">
      <div className="row-span-1 col-span-5 flex items-center">
        <div className="col-span-5 grid grid-cols-4 gap-3 p-4">
          <ForecastWeekSelect></ForecastWeekSelect>
          <div className="col-span-3 border-l-2 border-gray-200 flex items-center justify-start gap-3 pl-3">
            <PeopleIcon width={24} height={24}></PeopleIcon>
            <span>32 departments</span>
          </div>
        </div>
      </div>
      <div className="row-span-12 col-span-5 grid grid-cols-3 gap-3 p-4 h-full">
        <div className="col-span-2 border border-gray-200 rounded-xl">
          <DengueMap></DengueMap>
        </div>
        <div className="col-span-1 grid grid-rows-9 p-4 gap-3 border border-gray-200 rounded-xl bg-white">
          <div className="row-span-1 flex flex-col gap-2">
            <span className="text-black text-2xl">Select a department</span>
            <span className="text-gray-300 text-xl">Click a department on the map to view its forecast.</span>
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
