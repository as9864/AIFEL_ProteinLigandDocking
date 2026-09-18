"""Data-loading utilities for virtual-screening benchmark datasets
(DUD-E, LIT-PCBA) and a PDBbind-substitute real-binder reference (RCSB API).

Split out from the personal ProteinAnomalyDetection project — this package
here only carries the data-acquisition/loading layer, not the bias metrics
or diagnosis pipeline built on top of it.
"""

__all__ = ["features", "datasets"]
