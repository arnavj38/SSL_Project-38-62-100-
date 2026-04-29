#!/usr/bin/env bash

# file where all match results are stored
HISTORY_CSV="history.csv"

# take sorting argument from command line (default = wins)
SORT_BY="${1:-wins}"

# decide which column to sort on
# 3 = wins, 4 = losses, 5 = ratio
SORT_COL=3
[[ "$SORT_BY" == "losses" ]] && SORT_COL=4
[[ "$SORT_BY" == "ratio"  ]] && SORT_COL=5

echo ""
echo "          LEADERBOARD (sorted by: $SORT_BY)        "
echo ""

# print table headers
printf "%-15s %-12s %-8s %-8s %-10s\n" "Player" "Game" "Wins" "Losses" "W/L Ratio"
printf "%-15s %-12s %-8s %-8s %-10s\n" "---------------" "------------" "--------" "--------" "----------"

# use awk to process csv file
awk -F',' '
{
    winner = $1
    loser  = $2
    game   = $4

    # remove carriage return characters (windows issue)
    gsub(/\r/, "", winner)
    gsub(/\r/, "", loser)
    gsub(/\r/, "", game)

    # remove extra spaces from start and end
    gsub(/^ +| +$/, "", winner)
    gsub(/^ +| +$/, "", loser)
    gsub(/^ +| +$/, "", game)

    # skip invalid rows (empty / draw / exit)
    if (winner == "" || loser == "") next
    if (winner == "Draw" && loser == "Draw") next
    if (winner == "None" || loser == "None") next

    # make unique key using player + game
    key_w = winner "|" game
    key_l = loser  "|" game

    # count wins and losses
    wins[key_w]++
    losses[key_l]++

    # mark this key as seen
    seen[key_w] = 1
    seen[key_l] = 1
}
END {
    # loop through all players and games
    for (key in seen) {
        split(key, parts, "|")
        player = parts[1]
        game   = parts[2]

        w = wins[key] + 0
        l = losses[key] + 0

        # calculate win/loss ratio
        # if no losses, set a large value so it goes on top
        ratio = (l > 0) ? w/l : (w > 0 ? 9999 : 0)

        # print in pipe-separated format (for sorting)
        printf "%s|%s|%d|%d|%.2f\n", player, game, w, l, ratio
    }
}
' "$HISTORY_CSV" |

# sort based on chosen column (descending)
sort -t'|' -k"${SORT_COL}","${SORT_COL}"rn |

# final formatting for clean table output
awk -F'|' '{
    # show "Inf" instead of large number
    ratio = ($5 >= 9999) ? "Inf" : sprintf("%.2f", $5)

    printf "%-15s %-12s %-8s %-8s %-10s\n", $1, $2, $3, $4, ratio
}'

echo ""