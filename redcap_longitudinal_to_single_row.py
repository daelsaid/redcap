"""

This script will collapse all events into 1 specific row (generlaly the enrollment row), and the data that gets moved into that column will have the event name it came from appended to the variable its associated with: 
  e.g., fsiq from np1_yr0_arm_1 becomes fsiq_np1_yr0_arm_1

Usage:
    python /Users/daelsaid/scripts/github/redcap/redcap_longitudinal_to_single_row.py \
        --input  redcap_raw_exportfile.csv \
        --output [outputfilename.csv \
        --anchor enrollment_arm_1 (could be other event if enrollment isnt in your project.)

    #dev/ in progress to include any other arm: # Or just run with defaults (looks for any *_arm_1 anchor):
    python redcap_longitudinal_to_wide.py --input your_export.csv
"""

import pandas as pd
import argparse
import os


def redcap_longitudinal_to_single_row(
    input_path: str,
    output_path: str = None,
    anchor_event: str = "enrollment_arm_1",
    record_id_col: str = "record_id",
    event_col: str = "redcap_event_name",
    drop_all_na_cols: bool = True,
) -> pd.DataFrame:
    """
    Parameters
    ----------
    input_path     : Path to the REDCap CSV export.
    output_path    : Where to save the wide CSV. If None, saves in same location as the input.
    anchor_event   : The event whose columns stay without a suffix.
                     All other events are appended as [var]_<event_name>.
    record_id_col  : Column name for the subject/record ID.
    event_col      : Column name for the REDCap event.
    drop_all_na_cols: Drop columns that have no data (NaN) in the final output.

    Returns
    -------
    Wide-format DataFrame (one row per subject).
    """
    df = pd.read_csv(input_path, dtype=str)  # read as str to preserve NC/NA strings

    if event_col not in df.columns:
        raise ValueError(f"Event column '{event_col}' not found. Available: {list(df.columns)}")
    if record_id_col not in df.columns:
        raise ValueError(f"Record ID column '{record_id_col}' not found.")

    events = df[event_col].unique()
    print(f"Found {len(events)} events: {list(events)}")
    print(f"Anchor event: {anchor_event}")

    # Data columns (everything except record_id and event)
    data_cols = [c for c in df.columns if c not in [record_id_col, event_col]]

    # ── Build wide dataframe per subject ──────────────────────────────────────
    all_wide = []

    for record, subject_df in df.groupby(record_id_col):
        subject_df = subject_df.set_index(event_col)
        row = {record_id_col: record}

        for event in subject_df.index:
            event_row = subject_df.loc[event]

            for col in data_cols:
                val = event_row[col] if col in event_row.index else None

                if event == anchor_event:
                    # Anchor columns keep their original name
                    new_col = col
                else:
                    # Suffix non-anchor columns with the event name
                    new_col = f"{col}_{event}"

                # Anchor values take priority; don't overwrite with NaN from other events
                if new_col not in row or (pd.isna(row[new_col]) or row[new_col] == ""):
                    row[new_col] = val

        all_wide.append(row)

    wide_df = pd.DataFrame(all_wide)

    # Drop empty columns (optional)
    if drop_all_na_cols:
        before = wide_df.shape[1]
        wide_df.replace("", pd.NA, inplace=True)
        wide_df.dropna(axis=1, how="all", inplace=True)
        print(f"Dropped {before - wide_df.shape[1]} all-NaN columns.")

    print(f"\nResult: {wide_df.shape[0]} subjects × {wide_df.shape[1]} columns")

    # ── Save ──────────────────────────────────────────────────────────────────
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = base + "_wide.csv"

    wide_df.to_csv(output_path, index=False)
    print(f"Saved → {output_path}")

    return wide_df


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="REDCap longitudinal → wide format")
    parser.add_argument("--input",   required=True, help="Path to REDCap CSV export")
    parser.add_argument("--output",  default=None,  help="Output CSV path (optional)")
    parser.add_argument("--anchor",  default="enrollment_arm_1",
                        help="Anchor event name (default: enrollment_arm_1)")
    parser.add_argument("--record_id", default="record_id",
                        help="Record ID column name (default: record_id)")
    parser.add_argument("--event_col", default="redcap_event_name",
                        help="Event column name (default: redcap_event_name)")
    parser.add_argument("--keep_empty_cols", action="store_true",
                        help="Keep columns that are entirely NaN")
    args = parser.parse_args()

    redcap_longitudinal_to_single_row(
        input_path=args.input,
        output_path=args.output,
        anchor_event=args.anchor,
        record_id_col=args.record_id,
        event_col=args.event_col,
        drop_all_na_cols=not args.keep_empty_cols,
    )