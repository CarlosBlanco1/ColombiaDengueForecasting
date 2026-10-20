export function ForecastWeekSelect() {
    return <>
        <div className="flex items-center gap-4">
            <span className="text-lg font-semibold">Forecast week</span>
            <div>
                <select className="bg-white p-2 border border-gray-200 rounded-xl font-semibold">
                    <option value={"[2026, 42]"}>2026 * Week 42</option>
                </select>
            </div>
        </div>
    </>
}