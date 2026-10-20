export function ForecastWeekSelect() {
    return <>
        <div className="flex items-center gap-4">
            <span className="text-xl font-semibold">Forecast week</span>
            <div>
                <select className="bg-[#FDFCFB] p-2 border border-gray-200 rounded-xl font-semibold">
                    <option value={"[2026, 42]"}>2026 &#x2022; Week 42</option>
                </select>
            </div>
        </div>
    </>
}