## memo
   一番右側から連続してる0の数だけ右にシフト
   x / (x & -x)

## hand
 0 HighCard
 1 OnePair
 2 TwoPair
 3 ThreeOfAKind
 6 FullHouse
 7 FourOfAKind
 4 Straight
 5 Flush
 8 StraightFlush
 9 Royal Straight Flush

### テストコマンド
python -m unittest tests\test_calc.py

### 処理時間計測
python -m cProfile -s cumulative file_name.py
