import { InfoIcon } from "./icons/InfoIcon";

export function PredictedCasesCard() {
    return <>
        <div className="border rounded-xl border-gray-100 grid grid-rows-9 p-4 h-full">
            <div className="row-span-1 grid grid-cols-17">
                <span className="text-black col-span-16 font-black text-2xl">Predicted dengue cases</span>
                <div className="rounded-2xl bg-card-gray col-span-1 flex items-center justify-center">
                    <InfoIcon></InfoIcon>
                </div>
            </div>
            <div className="row-span-5">
                GRAPH GOES HERE
            </div>
            <div className="row-span-4 rounded-xl text-title-gray bg-card-gray text-center">
                Select a department to view the forecast time series.
            </div>
        </div>
    </>
}