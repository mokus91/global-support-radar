#!/usr/bin/env python3
"""Daily Spanish grant-call discovery using the official SNPSAP/BDNS API.\n\nOnly active application windows are published; historic awards are excluded."""
import json, re, sys, time
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
BASE="https://www.infosubvenciones.es/bdnstrans/api"
PORTAL="https://www.infosubvenciones.es/bdnstrans/GE/es"
TODAY=date.today()
HEADERS={"User-Agent":"GlobalSupportRadar/1.0 (+https://mokus91.github.io/global-support-radar/)","Accept":"application/json"}
def get_json(path,params):
    url=BASE+path+"?"+urlencode(params,doseq=True)
    with urlopen(Request(url,headers=HEADERS),timeout=25) as r:
        if r.status!=200: raise RuntimeError(f"SNPSAP HTTP {r.status}")
        data=json.loads(r.read().decode("utf-8"))
    if not isinstance(data,dict): raise RuntimeError("Unexpected SNPSAP response")
    return data
def numeric_budget(value):
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return value if value >= 0 else None
    if isinstance(value, str):
        raw=value.strip().replace(" ", "")
        if not raw:
            return None
        # Spanish-formatted values commonly use dots for thousands and comma decimals.
        if "," in raw:
            raw=raw.replace(".", "").replace(",", ".")
        else:
            raw=raw.replace(".", "")
        try:
            number=float(raw)
            return number if number >= 0 else None
        except ValueError:
            return None
    return None

def categories(d):
    text=" ".join([str(d.get("descripcion") or ""),str(d.get("descripcionFinalidad") or ""),
      " ".join(x.get("descripcion","") for x in d.get("sectores",[]) if isinstance(x,dict)),
      " ".join(x.get("descripcion","") for x in d.get("objetivos",[]) if isinstance(x,dict))]).lower()
    rules=[("agriculture",("agricultur","ganader","pesca","silvicultur","agrari")),
      ("housing",("vivienda","alquiler","hogar")),("family",("familia","natalidad","infancia","conciliación")),
      ("education",("educación","educativ","beca","estudios","formación")),("healthcare",("sanidad","salud","sanitari","hospital")),
      ("energy",("energía","renovable","eficiencia energética","autoconsumo")),("employment",("empleo","desemple","contratación","inserción laboral")),
      ("transport",("transporte","movilidad","vehículo eléctrico")),("social_support",("servicios sociales","inclusión social","discapacidad","dependencia","pobreza")),
      ("business",("empresa","empresarial","pyme","autónom","emprend","industria","comercio","innovación","investigación"))]
    found=[k for k,words in rules if any(w in text for w in words)]
    return found or ["all"]
def main():
    listing=get_json("/convocatorias/ultimas",{"page":0,"pageSize":50,"order":"fechaRecepcion","direccion":"desc","vpd":"GE"})
    items=listing.get("content")
    if not isinstance(items,list): raise RuntimeError("SNPSAP latest calls has no content list")
    records=[]; errors=[]; checked=0
    for item in items[:50]:
        code=str(item.get("numeroConvocatoria") or "").strip()
        if not re.fullmatch(r"[0-9A-Za-z-]+",code): continue
        try:
            d=get_json("/convocatorias",{"vpd":"GE","numConv":code})
            if isinstance(d.get("content"),dict): d=d["content"]
            checked+=1
            start=d.get("fechaInicioSolicitud"); end=d.get("fechaFinSolicitud")
            sd=date.fromisoformat(start[:10]) if start else None
            ed=date.fromisoformat(end[:10]) if end else None
            indefinite=d.get("abierto") is True
            active=(sd is None or sd<=TODAY) and (ed is None or ed>=TODAY)
            if not active or not (indefinite or (sd and ed)): continue
            title=str(d.get("descripcion") or item.get("descripcion") or "").strip()
            if not title: continue
            org=d.get("organo") if isinstance(d.get("organo"),dict) else {}
            regions=[x.get("descripcion") for x in d.get("regiones",[]) if isinstance(x,dict) and x.get("descripcion")]
            beneficiaries=[x.get("descripcion") for x in d.get("tiposBeneficiarios",[]) if isinstance(x,dict) and x.get("descripcion")]
            budget_raw=d.get("presupuestoTotal")\n            budget=numeric_budget(budget_raw)
            records.append({"id":code,"country_code":"ES","title_original":title,"coofficial_title":d.get("descripcionLeng"),
              "publisher":"Spain National Transparency Register for Public Grants and Public Aid (SNPSAP/BDNS)",
              "granting_authority":" · ".join(x for x in [org.get("nivel1"),org.get("nivel2"),org.get("nivel3")] if x),
              "regions":regions,"eligible_beneficiaries_original":beneficiaries,"eligibility_status":"beneficiary_types_listed_in_official_api" if beneficiaries else "not_specified_in_api","purpose_original":d.get("descripcionFinalidad"),
              "start_date":start,"deadline":end,"indefinite_open":indefinite,"total_call_budget":budget,"total_call_budget_original":budget_raw,
              "amount_currency":"EUR" if budget is not None else None,"amount_type":"total_call_budget_not_individual_award" if budget is not None else None,"amount_status":"published" if budget is not None else "source_field_untyped" if budget_raw not in (None, "") else "not_published","categories":categories(d),
              "official_url":f"{PORTAL}/convocatoria/{code}","application_url":d.get("sedeElectronica"),
              "legal_bases_url":d.get("urlBasesReguladoras"),"status":"official-api-window-current",
              "eligibility_verified":False,"amount_verified":False,"source_api":BASE,
              "note_hu":"Az API szerinti jelentkezési időszak jelenleg aktív vagy határozatlan idejű. A teljes pályázati keret nem az egy pályázónak járó összeg. A részletes feltételeket az eredeti kiírásban ellenőrizd.",
              "note_en":"The API indicates a current or indefinite application window. The published total call budget is not an individual award. Beneficiary categories are copied from the official API but do not establish an individual applicant eligibility. Verify full terms in the original notice."})
        except Exception as e: errors.append({"id":code,"error":str(e)[:200]})
        time.sleep(0.2)
    out={"generated_at":datetime.now(timezone.utc).isoformat(),"country_code":"ES","source":BASE,
      "records_checked":checked,"records_count":len(records),"query_errors":errors[:10],"records":records,
      "coverage_note":"Only the 50 most recently registered calls are checked daily. Status is derived from official application dates and the API's indefinite-open flag; this is not exhaustive."}
    Path("data").mkdir(exist_ok=True)
    Path("data/spain-discovery.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"SNPSAP: checked {checked}; active-window candidates {len(records)}; detail errors {len(errors)}")
if __name__=="__main__":
    try: main()
    except Exception as e:
        print(f"SNPSAP discovery failed: {e}",file=sys.stderr); raise
