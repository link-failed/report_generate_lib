with i as
(
  select
    subject_id, icustay_id
  FROM icustays
)
, iid_assign as
(
  select
    subject_id, icustay_id
    from i
)
, pvt as
( -- begin query that extracts the data
  select le.hadm_id, charttime
    FROM labevents le
)
, grp as
(
  select pvt.hadm_id, pvt.charttime
  from pvt
  group by pvt.hadm_id, pvt.charttime
  having sum(case when label = 'SPECIMEN' then 1 else 0 end)<2
)
select
  iid.icustay_id, grp.*
from grp
inner join admissions adm
  on grp.hadm_id = adm.hadm_id
left join iid_assign iid
  on adm.subject_id = iid.subject_id
  and grp.charttime >= iid.data_start
  and grp.charttime < iid.data_end
order by grp.hadm_id, grp.charttime
