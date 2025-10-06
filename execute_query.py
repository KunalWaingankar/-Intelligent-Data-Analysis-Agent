import pandas as pd

def execute_query(df: pd.DataFrame, query_dict: dict):
  try:
      if "error" in query_dict:
          return query_dict["error"]

      df_filtered = df.copy()

      if 'region' in query_dict.get('filter', {}) and not query_dict.get('group_by'):
          group_col = 'region'
      else:
          group_col = query_dict.get('group_by')


      metadata_map = {
          "editions": lambda df: df['Year'].nunique() if 'Year' in df.columns else None,
          "hosts": lambda df: df['City'].nunique() if 'City' in df.columns else None,
          "sports": lambda df: df['Sport'].nunique() if 'Sport' in df.columns else None,
          "events": lambda df: df['Event'].nunique() if 'Event' in df.columns else None,
          "nations": lambda df: df['region'].nunique() if 'region' in df.columns else None,
          "athletes": lambda df: df['Name'].nunique() if 'Name' in df.columns else None
      }

      # Check metadata
      if query_dict.get("operation") == "metadata":
          key = query_dict.get("metadata_key")
          if key in metadata_map:
              return {key: metadata_map[key](df_filtered)}
          else:
              return f"Metadata key '{key}' not recognized."

      # Drop duplicates for region/group_by sum
      if query_dict.get("group_by") == 'region' or (not query_dict.get("group_by") and query_dict.get("operation") == "sum"):
          df_filtered = df_filtered.drop_duplicates(
              subset=['Team', 'NOC', 'Year', 'Sport', 'Event', 'Medal']
          )

      # -------------------------
      # Apply filters including Gender for numerical operations
      # -------------------------
      filters = query_dict.get("filter", {})
      gender_filter = query_dict.get("gender") or filters.pop("Sex", None)

      for key, value in filters.items():
          if key in df_filtered.columns:
              if isinstance(value, list) and len(value) == 2:
                  df_filtered = df_filtered[
                      (df_filtered[key] >= value[0]) & (df_filtered[key] <= value[1])
                  ]
              else:
                  df_filtered = df_filtered[df_filtered[key] == value]

      if gender_filter and "Sex" in df_filtered.columns:
          df_filtered = df_filtered[df_filtered["Sex"] == gender_filter]

      cols = query_dict.get("columns") or [query_dict.get("column")]
      cols = [c for c in cols if c in df_filtered.columns]

      group_col = query_dict.get("group_by")
      op = query_dict.get("operation")
      top_n = query_dict.get("top_n", 1)  # Default to 1

      # -------------------------
      # Gender_stats counting
      # -------------------------
      if op == "gender_stats":
          if "Sex" not in df_filtered.columns or "Name" not in df_filtered.columns:
              return "Error: Dataset requires 'Sex' and 'Name' columns for gender analysis."

          # Drop duplicates to count unique athletes
          df_filtered = df_filtered.drop_duplicates(subset=['Year','Event','Name','Team'])
          count = df_filtered["Name"].nunique()
          return {f"Total {gender_filter} Athletes": int(count)}

      # -------------------------
      # Group by logic
      # -------------------------
      if group_col:
          if not cols:
              return "Error: No valid column found for operation."
          
          # Drop duplicates first for count
          if op == "count":
              unique_cols = [group_col] + cols
              df_filtered = df_filtered.drop_duplicates(subset=unique_cols)
              grouped = df_filtered.groupby(group_col)[cols[0]].nunique().reset_index()
              result = grouped

          else:
              grouped = df_filtered.groupby(group_col)[cols]

              if op == "sum":
                  result = grouped.sum().reset_index()
              elif op == "mean":
                  result = grouped.mean().reset_index()
              elif op == "max":
                  result = grouped.max().reset_index()
              elif op == "min":
                  result = grouped.min().reset_index()
              elif op == "top":
                  result = grouped.sum().reset_index()
                  main_col = cols[0]

                  if "top_n" in query_dict:
                      n = query_dict["top_n"]
                      result = result.sort_values(main_col, ascending=False).head(n).reset_index(drop=True)

                  elif "nth_place" in query_dict:
                      n = query_dict["nth_place"]
                      result = result.sort_values(main_col, ascending=False).iloc[[n-1]].reset_index(drop=True)

                  else:
                      # default to top 1
                      result = result.sort_values(main_col, ascending=False).head(1).reset_index(drop=True)
              else:
                  result = "Operation not recognized."

          if isinstance(result, pd.DataFrame) and "Gold" in result.columns and op != "top":
              result = result.sort_values("Gold", ascending=False).reset_index(drop=True)

      else:
          # No group by, applying aggregation directly
          if not cols:
              return "Error: No valid column found for operation."

          if op == "sum":
              result = df_filtered[cols].sum().to_dict()
          elif op == "mean":
              df_filtered = df_filtered.drop_duplicates(subset=['Year','Event','Medal','Team','NOC'])
              num_years = df_filtered['Year'].nunique()
              total = df_filtered[cols].sum()
              result = (total / num_years).to_dict()
          elif op == "max":
              result = df_filtered[cols].max().to_dict()
          elif op == "min":
              result = df_filtered[cols].min().to_dict()
          elif op == "count":
              # Count unique after removing duplicates
              df_filtered = df_filtered.drop_duplicates(subset=cols)
              result = {cols[0]: int(df_filtered[cols[0]].nunique())}
          else:
              result = "Operation not recognized."

      return result

  except Exception as e:
      return f"Error executing query: {e}"