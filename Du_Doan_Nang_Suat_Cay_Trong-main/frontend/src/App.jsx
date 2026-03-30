import { useState } from 'react'

function App() {
  const [formData, setFormData] = useState({
    Region: 'Miền Bắc',
    Soil_Type: 'Đất Cát',
    Crop: 'Lúa',
    Rainfall_mm: '',
    Temperature_Celsius: '',
    N: '',
    P: '',
    K: '',
    Irrigation_Used: '0',
    Weather_Condition: 'Nắng',
    Days_to_Harvest: '',
    Selected_Model: 'Transformer'
  })

  const [predictionResult, setPredictionResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setPredictionResult(null)
    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || 'Có lỗi xảy ra từ server.')
      setPredictionResult({ value: data.prediction, model: data.model })
    } catch (err) {
      setError(err.message || 'Không thể kết nối đến server.')
    } finally {
      setLoading(false)
    }
  }

  return (
    // THAY ĐỔI CHÍNH: Nền Gradient xanh tươi (Emerald -> Teal)
    <div className="min-h-screen relative flex items-center justify-center font-sans py-20 px-6 overflow-x-hidden bg-gradient-to-br from-emerald-50 via-green-100 to-teal-100">

      <div className="relative z-10 max-w-6xl w-full">
        {/* Header Section - Rộng rãi và phân cấp cao */}
        <header className="text-center mb-16 text-slate-900">
          <h1 className="text-5xl md:text-6xl font-black mb-4 tracking-tighter drop-shadow-sm">
            AgroPredict <span className="text-emerald-600">AI</span>
          </h1>
          <p className="text-lg md:text-xl text-slate-700 font-medium max-w-2xl mx-auto opacity-90">
            Ứng dụng công nghệ học máy để tối ưu hóa năng suất nông nghiệp dựa trên dữ liệu thổ nhưỡng và khí hậu.
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Grid chính - Chia 2 cột lớn */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

            {/* CỘT TRÁI: ĐỊA LÝ & MÔI TRƯỜNG */}
            <section className="bg-white/95 backdrop-blur-xl rounded-[2.5rem] p-10 shadow-2xl shadow-emerald-950/5 border border-white/20 hover:shadow-emerald-950/10 transition-shadow duration-300">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 bg-emerald-100 rounded-2xl flex items-center justify-center text-emerald-600 border border-emerald-200">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-slate-800 tracking-tight">Môi trường & Địa lý</h2>
                  <p className="text-sm text-slate-500 font-medium">Thông tin vùng miền và khí hậu</p>
                </div>
              </div>

              <div className="space-y-6">
                <div className="grid grid-cols-1 gap-6">
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase ml-1 tracking-wider">Vùng miền canh tác</label>
                    <select name="Region" value={formData.Region} onChange={handleChange} className="w-full bg-slate-50 border-2 border-slate-100 focus:border-emerald-400 focus:bg-white rounded-2xl p-4 transition-all outline-none text-slate-700 font-semibold shadow-inner">
                      <option value="Miền Bắc">Miền Bắc</option>
                      <option value="Miền Nam">Miền Nam</option>
                      <option value="Tây Nguyên">Tây Nguyên</option>
                      <option value="Duyên hải miền Trung">Duyên hải miền Trung</option>
                    </select>
                  </div>

                  <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-500 uppercase ml-1 tracking-wider">Loại đất</label>
                      <select name="Soil_Type" value={formData.Soil_Type} onChange={handleChange} className="w-full bg-slate-50 border-2 border-slate-100 focus:border-emerald-400 focus:bg-white rounded-2xl p-4 outline-none font-semibold shadow-inner">
                        <option value="Đất Cát">Đất Cát</option>
                        <option value="Đất Sét">Đất Sét</option>
                        <option value="Đất Bùn">Đất Bùn</option>
                      </select>
                    </div>
                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-500 uppercase ml-1 tracking-wider">Cây trồng</label>
                      <select name="Crop" value={formData.Crop} onChange={handleChange} className="w-full bg-slate-50 border-2 border-slate-100 focus:border-emerald-400 focus:bg-white rounded-2xl p-4 outline-none font-semibold shadow-inner">
                        <option value="Lúa">Lúa</option>
                        <option value="Ngô">Ngô</option>
                        <option value="Đậu nành">Đậu nành</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-500 uppercase ml-1 tracking-wider">Lượng mưa (mm)</label>
                      <input type="number" name="Rainfall_mm" value={formData.Rainfall_mm} onChange={handleChange} required placeholder="250" className="w-full bg-slate-50 border-2 border-slate-100 focus:border-emerald-400 focus:bg-white rounded-2xl p-4 outline-none font-semibold shadow-inner placeholder:text-slate-300" />
                    </div>
                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-500 uppercase ml-1 tracking-wider">Nhiệt độ (°C)</label>
                      <input type="number" name="Temperature_Celsius" value={formData.Temperature_Celsius} onChange={handleChange} required placeholder="28" className="w-full bg-slate-50 border-2 border-slate-100 focus:border-emerald-400 focus:bg-white rounded-2xl p-4 outline-none font-semibold shadow-inner placeholder:text-slate-300" />
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* CỘT PHẢI: DINH DƯỠNG & QUY TRÌNH */}
            <section className="bg-white/95 backdrop-blur-xl rounded-[2.5rem] p-10 shadow-2xl shadow-emerald-950/5 border border-white/20 flex flex-col hover:shadow-emerald-950/10 transition-shadow duration-300">
              <div className="flex items-center gap-4 mb-8">
                <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center text-blue-600 border border-blue-200">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                  </svg>
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-slate-800 tracking-tight">Dinh dưỡng & Quy trình</h2>
                  <p className="text-sm text-slate-500 font-medium">Thông số hóa lý và thời gian</p>
                </div>
              </div>

              <div className="space-y-8 flex-grow">
                {/* Chỉ số NPK rộng rãi */}
                <div className="grid grid-cols-3 gap-4">
                  {[
                    { label: 'Nitơ (N)', name: 'N', color: 'bg-orange-50 text-orange-600 border-orange-100 focus-within:border-orange-300' },
                    { label: 'Phốt pho (P)', name: 'P', color: 'bg-blue-50 text-blue-600 border-blue-100 focus-within:border-blue-300' },
                    { label: 'Kali (K)', name: 'K', color: 'bg-purple-50 text-purple-600 border-purple-100 focus-within:border-purple-300' }
                  ].map((field) => (
                    <div key={field.name} className={`${field.color} p-5 rounded-3xl border-2 flex flex-col items-center transition-all hover:scale-[1.03] shadow-inner`}>
                      <span className="text-[11px] font-black uppercase mb-3 opacity-80 tracking-widest">{field.label}</span>
                      <input type="number" name={field.name} value={formData[field.name]} onChange={handleChange} required className="w-full bg-transparent text-center text-3xl font-black outline-none placeholder:text-current/30" placeholder="0" />
                    </div>
                  ))}
                </div>

                <div className="space-y-6">
                  <div className="space-y-3">
                    <label className="text-xs font-bold text-slate-500 uppercase ml-1 text-center block tracking-wider">Tình trạng thời tiết hiện tại</label>
                    <div className="flex p-1.5 bg-slate-100 rounded-[1.5rem] gap-2 shadow-inner border border-slate-200">
                      {['Nắng', 'Mưa', 'Âm u'].map((item) => (
                        <button
                          key={item}
                          type="button"
                          onClick={() => setFormData({ ...formData, Weather_Condition: item })}
                          className={`flex-1 py-3 rounded-xl text-sm font-bold transition-all ${formData.Weather_Condition === item ? 'bg-white text-emerald-600 shadow border border-emerald-100' : 'text-slate-400 hover:text-slate-600'}`}
                        >
                          {item}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase ml-1 tracking-wider">Ngày thu hoạch dự kiến</label>
                    <input type="number" name="Days_to_Harvest" value={formData.Days_to_Harvest} onChange={handleChange} required className="w-full bg-slate-50 border-2 border-slate-100 focus:border-emerald-400 focus:bg-white rounded-2xl p-4 outline-none font-semibold text-center shadow-inner placeholder:text-slate-300" placeholder="60 - 300 ngày" />
                  </div>
                </div>
              </div>

              {/* Dropdown chọn Model */}
              <div className="mt-6">
                <label className="text-xs font-bold text-slate-500 uppercase ml-1 tracking-wider">Mô hình AI dự đoán</label>
                <select name="Selected_Model" value={formData.Selected_Model} onChange={handleChange} className="w-full mt-2 bg-emerald-50/50 border-2 border-emerald-100 focus:border-emerald-400 focus:bg-white rounded-2xl p-4 outline-none font-bold text-emerald-800 shadow-inner transition-all cursor-pointer">
                  <option value="Transformer">Transformer</option>
                  <option value="Autoformer">Autoformer</option>
                  <option value="XGBoost">XGBoost</option>
                  <option value="LightGBM">LightGBM</option>
                  <option value="Random Forest">Random Forest</option>
                  <option value="Neural Network">Neural Network</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full mt-10 bg-emerald-600 hover:bg-emerald-700 text-white py-5 rounded-2xl font-black text-xl shadow-lg shadow-emerald-500/30 transition-all active:scale-[0.98] flex items-center justify-center gap-3 disabled:opacity-60"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span>ĐANG PHÂN TÍCH...</span>
                  </>
                ) : (
                  <>
                    <span>DỰ ĐOÁN NGAY</span>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </>
                )}
              </button>
            </section>
          </div>
        </form>

        {/* AREA KẾT QUẢ - TÁCH BIỆT RÕ RÀNG */}
        <div className="mt-12 max-w-2xl mx-auto">
          {error && (
            <div className="p-6 bg-red-500 text-white rounded-[2rem] shadow-xl shadow-red-500/20 flex items-center gap-4 animate-shake">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor font-bold">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <p className="font-bold text-lg">{error}</p>
            </div>
          )}

          {predictionResult !== null && (
            <div className="bg-emerald-500 p-[2px] rounded-[3rem] shadow-[0_30px_60px_-15px_rgba(16,185,129,0.3)]">
              <div className="bg-slate-950 rounded-[2.9rem] p-10 relative overflow-hidden">
                <div className="relative z-10">
                  <div className="text-center">
                    <span className="inline-block px-4 py-1.5 bg-emerald-400 text-emerald-950 rounded-full text-xs font-black mb-6 uppercase tracking-tight shadow">
                      Phân tích thành công
                    </span>
                    <h3 className="text-slate-400 text-sm font-bold uppercase tracking-widest mb-2">Năng suất ước tính</h3>
                    <p className="text-emerald-400 font-medium mb-6">Mô hình: {predictionResult.model}</p>
                    <div className="flex items-center justify-center gap-3">
                      <span className="text-8xl font-black text-white tabular-nums tracking-tighter drop-shadow-lg">{predictionResult.value}</span>
                      <span className="text-2xl font-medium text-emerald-400 leading-tight">tấn<br /><span className="text-slate-500">trên ha</span></span>
                    </div>
                    <p className="mt-8 text-center text-slate-500 text-xs max-w-sm mx-auto opacity-70">Dự đoán này dựa trên mô hình trí tuệ nhân tạo được huấn luyện với dữ liệu nông nghiệp thực tế.</p>
                  </div>
                </div>
                {/* Decorative Elements */}
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent opacity-50"></div>
                <div className="absolute -bottom-20 -right-20 w-64 h-64 bg-emerald-400/10 rounded-full blur-[80px]"></div>
                <div className="absolute -top-20 -left-20 w-64 h-64 bg-emerald-400/5 rounded-full blur-[80px]"></div>
              </div>
            </div>
          )}
        </div>


      </div>
    </div>
  )
}

export default App