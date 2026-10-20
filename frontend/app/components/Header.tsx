import { CalendarIcon } from "./icons/CalendarIcon";
import Image from "next/image";


export function Header() {
    return <>
        <div className="grid grid-cols-3 text-title-green py-3">
            <div className="grid grid-cols-8 items-center">
                <div className="col-span-1 flex items-center justify-center">
                    <Image
                        className="h-13 w-auto"
                        src="/icon.png"
                        alt="Header logo"
                        width={140}
                        height={103}
                        priority
                    />
                </div>
                <span className="col-span-7 text-2xl font-bold">
                    Dengue Forecast Colombia
                </span>
            </div>
            <div className="flex items-center justify-center text-md">
                <div className="grid grid-cols-3 gap-3 justify-center">
                    <div className="flex items-center justify-center">
                        <span className="py-2 border-b-4 text-center font-semibold">Forecast</span>
                    </div>
                    <div className="flex items-center justify-center">
                        <span className="py-2 border-b-4 text-center font-semibold">Methodology</span>
                    </div>
                    <div className="flex items-center justify-center">
                        <span className="py-2 border-b-4 text-center font-semibold">Data</span>
                    </div>
                </div>
            </div>
            <div className="flex items-center justify-end pr-2">
                <div className="grid grid-cols-5 py-2 px-3 rounded-3xl bg-green-200 gap-2">
                    <span className="col-span-1">
                        <CalendarIcon width={24} height={24}></CalendarIcon>
                    </span>
                    <span className="col-span-4 text-center text-lg font-semibold">
                        Weekly outlook
                    </span>
                </div>
            </div>
        </div>
        <hr className="border border-gray-200"></hr>
    </>
}