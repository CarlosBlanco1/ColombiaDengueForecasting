import { InfoIcon } from "./icons/InfoIcon";

export function PredictedCasesCard() {
    return <>
        <div className="border rounded-xl border-gray-300 grid grid-rows-9 p-4 h-full">
            <div className="row-span-1 grid grid-cols-17">
                <span className="text-black col-span-16 font-semibold text-2xl">Predicted dengue cases</span>
                <div className="col-span-1 flex items-center justify-center text-gray-400">
                    <InfoIcon width={36} height={36}></InfoIcon>
                </div>
            </div>
            <div className="row-span-5">
                GRAPH GOES HERE
            </div>
            <div className="row-span-4 rounded-xl text-title-gray text-xl bg-card-gray flex items-center justify-center">
                <span>Select a department to view the forecast time series.</span>
            </div>
        </div>
    </>
}