# AIFEL_ProteinLigandDocking

가상 스크리닝 벤치마크(DUD-E, LIT-PCBA)와 PDBbind 대체 참조 데이터를 **받아오고 로딩하는 부분만** 모아둔 공용 모듈입니다. 편향 진단 지표(물성/골격/AVE bias) 등 분석 로직은 별도 개인 저장소에 있고, 여기에는 팀이 공통으로 쓸 **데이터 확보 방법 + 데이터 로더**만 옮겨 왔습니다.

## 무엇이 들어있나

| 데이터셋 | 받는 방법 | 로더 |
|---|---|---|
| DUD-E | https://dude.docking.org/ 에서 타깃별 압축파일 다운로드 (무료, 등록 불요) | [`datasets/dude.py`](src/proteinanomaly/datasets/dude.py) |
| LIT-PCBA | https://drugdesign.unistra.fr/LIT-PCBA/ 에서 전체 타깃 묶음 다운로드 (무료) | [`datasets/litpcba.py`](src/proteinanomaly/datasets/litpcba.py) |
| PDBbind | http://www.pdbbind.org.cn/ (계정 등록 필요 — 자동화 불가 확인됨) | [`datasets/pdbbind.py`](src/proteinanomaly/datasets/pdbbind.py) (공식 포맷용, 계정 확보 시 사용) |
| PDBbind 대체 (RCSB API) | `data.rcsb.org`/`search.rcsb.org` 공개 API, 로그인 불요 | [`datasets/rcsb_affinity.py`](src/proteinanomaly/datasets/rcsb_affinity.py) + [`scripts/fetch_rcsb_binding_reference.py`](scripts/fetch_rcsb_binding_reference.py) |

자세한 다운로드/레이아웃 안내는 [`data/README.md`](data/README.md) 참고.

모든 로더는 공통 `MoleculeSet`([`features.py`](src/proteinanomaly/features.py))을 반환합니다 — SMILES 파싱, 물성 디스크립터, Murcko scaffold, Morgan fingerprint를 한 곳에서 다루는 데이터클래스로, 이후 어떤 분석(도킹 전처리, 필터링 등)에도 그대로 재사용할 수 있습니다.

## 설치

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash; PowerShell은 .venv\Scripts\Activate.ps1
pip install -e .
```

## 사용법

### DUD-E / LIT-PCBA 로딩

타깃별 압축파일을 받아 아래 레이아웃으로 배치한 뒤:

```
data/raw/dude/<target>/actives_final.ism
data/raw/dude/<target>/decoys_final.ism

data/raw/litpcba/<target>/actives.smi
data/raw/litpcba/<target>/inactives.smi
```

```python
from proteinanomaly.datasets import load_dude_target, load_litpcba_target

actives, decoys = load_dude_target("data/raw/dude", "ampc")
actives, inactives = load_litpcba_target("data/raw/litpcba", "TP53")

print(len(actives), "actives")
df = actives.descriptor_frame()   # 물성 디스크립터 DataFrame
scaffolds = actives.scaffolds()   # Bemis-Murcko scaffold SMILES 리스트
fps = actives.fingerprints()      # Morgan(ECFP4) fingerprint 리스트
```

### PDBbind 대체 참조 세트 (RCSB API)

PDBbind는 계정 로그인 없이는 자동 다운로드가 막혀 있어서, 실측 결합친화도가 붙은 복합체를 RCSB 공개 API로 대신 수집합니다.

```bash
python scripts/fetch_rcsb_binding_reference.py --limit 300 --out data/raw/rcsb_affinity/reference.csv
```

```python
from proteinanomaly.datasets import load_rcsb_affinity_reference

reference = load_rcsb_affinity_reference("data/raw/rcsb_affinity/reference.csv")
```

정식 PDBbind 계정을 확보하면 `datasets/pdbbind.py`(`load_pdbbind_index`, `load_pdbbind_ligand_smiles`)로 그대로 교체 가능하도록 동일한 `MoleculeSet` 인터페이스로 맞춰뒀습니다.

## 참고

배경/방법론 관련 전체 제안서는 [`doc/제안서.md`](doc/제안서.md) 참고.
