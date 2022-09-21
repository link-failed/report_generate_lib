select io.icustay_id, io.charttime
  , sum(case when DATETIME_DIFF(io.charttime, iosum.charttime, 'HOUR') <= 5
      then iosum.VALUE
    else null end) as urineoutput_6hr
  , sum(case when DATETIME_DIFF(io.charttime, iosum.charttime, 'HOUR') <= 11
      then iosum.VALUE
    else null end) as urineoutput_12hr
  -- 24 hours
  , sum(iosum.VALUE) as urineoutput_24hr

  , MIN(case when io.charttime <= DATETIME_ADD(iosum.charttime, INTERVAL '5 HOUR')
      then iosum.charttime
    else null end)
    AS starttime_6hr
  , MIN(case when io.charttime <= DATETIME_ADD(iosum.charttime, INTERVAL '11 HOUR')
      then iosum.charttime
    else null end)
    AS starttime_12hr
  , MIN(iosum.charttime) AS starttime_24hr
  from (
    (select * from {{ ref('urine_output') }} limit 672000 offset 672000) as io
    -- this join gives you all UO measurements over a 24 hour period
    left join {{ ref('urine_output') }} iosum
      on  io.icustay_id = iosum.icustay_id
      and io.charttime >= iosum.charttime
      and io.charttime <= (DATETIME_ADD(iosum.charttime, INTERVAL '23 HOUR'))
  )
  group by io.icustay_id, io.charttime
