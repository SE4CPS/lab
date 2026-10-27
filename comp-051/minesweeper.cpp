#include <iostream>
#include <cstdlib>
#include <ctime>

const int SIZE = 6;

int board[SIZE][SIZE];
bool revealed[SIZE][SIZE];

void initBoard(int b[SIZE][SIZE]);
void placeMines(int b[SIZE][SIZE], int n);
int countAdjacent(int b[SIZE][SIZE],
                  int r, int c);
void fillNumbers(int b[SIZE][SIZE]);

void initBoard(int b[SIZE][SIZE]) {
  for (int r = 0; r < SIZE; r++)
    for (int c = 0; c < SIZE; c++)
      b[r][c] = 0;
}

void placeMines(int b[SIZE][SIZE], int n) {
  int placed = 0;
  while (placed < n) {
    int r = rand() % SIZE;
    int c = rand() % SIZE;
    if (b[r][c] == -1) {
      continue;
    }
    b[r][c] = -1;
    placed++;
  }
}

int countAdjacent(int b[SIZE][SIZE],
                  int r, int c) {
  int count = 0;
  for (int dr = -1; dr <= 1; dr++) {
    for (int dc = -1; dc <= 1; dc++) {
      int nr = r + dr, nc = c + dc;
      if (dr == 0 && dc == 0) {
        continue;
      }
      if (nr < 0 || nr >= SIZE ||
          nc < 0 || nc >= SIZE) {
        continue;
      }
      if (b[nr][nc] == -1) {
        count++;
      }
    }
  }
  return count;
}

void fillNumbers(int b[SIZE][SIZE]) {
  for (int r = 0; r < SIZE; r++)
    for (int c = 0; c < SIZE; c++)
      if (b[r][c] != -1)
        b[r][c] = countAdjacent(b, r, c);
}

void printBoard(int b[SIZE][SIZE],
                bool rv[SIZE][SIZE]) {
  for (int r = 0; r < SIZE; r++) {
    for (int c = 0; c < SIZE; c++) {
      if (!rv[r][c]) {
        std::cout << '#';
      } else {
        std::cout << b[r][c];
      }
    }
    std::cout << "\n";
  }
}

bool revealCell(int b[SIZE][SIZE],
                bool rv[SIZE][SIZE],
                int r, int c) {
  rv[r][c] = true;
  return b[r][c] == -1;
}

bool isWon(int b[SIZE][SIZE],
            bool rv[SIZE][SIZE]) {
  for (int r = 0; r < SIZE; r++)
    for (int c = 0; c < SIZE; c++)
      if (b[r][c] != -1 && !rv[r][c])
        return false;
  return true;
}

int main() {
  srand(time(0));
  initBoard(board);
  placeMines(board, 6);
  fillNumbers(board);

  bool won = false;
  while (!won) {
    printBoard(board, revealed);

    int r, c;
    std::cout << "Row col: ";
    std::cin >> r >> c;

    bool hitMine = revealCell(board,
                              revealed, r, c);
    if (hitMine) {
      printBoard(board, revealed);
      std::cout << "Boom! You lost.";
      break;
    }

    won = isWon(board, revealed);
    if (won) {
      printBoard(board, revealed);
      std::cout << "You win!";
    }
  }
  return 0;
}
