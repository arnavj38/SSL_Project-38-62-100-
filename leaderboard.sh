#!/usr/bin/env bash

HISTORY_CSV="history.csv"
SORT_BY="$1"


# Map sort metric to column
SORT_COL=3
[[ "$SORT_BY" == "losses" ]] && SORT_COL=4
[[ "$SORT_BY" == "ratio"  ]] && SORT_COL=5

echo ""
echo "===== LEADERBOARD (sorted by: $SORT_BY) ====="
echo ""

printf "%-15s %-12s %-8s %-8s %-10s\n" "Player" "Game" "Wins" "Losses" "W/L Ratio"
printf "%-15s %-12s %-8s %-8s %-10s\n" "---------------" "------------" "--------" "--------" "----------"

awk -F',' '
{
    winner = $1
    loser  = $2
    game   = $4

    # clean data (important!)
    gsub(/\r/, "", winner)
    gsub(/\r/, "", loser)
    gsub(/\r/, "", game)

    gsub(/^ +| +$/, "", winner)
    gsub(/^ +| +$/, "", loser)
    gsub(/^ +| +$/, "", game)

    key_w = winner "|" game
    key_l = loser  "|" game

    # update stats
    wins[key_w]++
    losses[key_l]++

    seen[key_w] = 1
    seen[key_l] = 1
}
END {
    for (key in seen) {
        split(key, parts, "|")
        player = parts[1]
        game   = parts[2]

        w = wins[key] + 0
        l = losses[key] + 0

        ratio = (l > 0) ? w/l : (w > 0 ? 9999 : 0)

        printf "%s|%s|%d|%d|%.2f\n", player, game, w, l, ratio
    }
}
' "$HISTORY_CSV" | sort -t'|' -k"${SORT_COL}","${SORT_COL}"rn | awk -F'|' '{
    ratio = ($5 >= 9999) ? "Inf" : sprintf("%.2f", $5)
    printf "%-15s %-12s %-8s %-8s %-10s\n", $1, $2, $3, $4, ratio
}'

echo ""