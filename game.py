from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

BOARD_SIZE = 8

@dataclass(frozen=True)
class Pos:
    rank: int
    file: int

    def __str__(self):
        return chr(0x41 + self.file) + str(self.rank + 1) # 0x41 is codepoint for 'A'
    
    def __getitem__(self, idx):
        if idx == 0:
            return self.rank
        elif idx == 1:
            return self.file
        else:
            raise IndexError("index must be 0 or 1")

    def __add__(self, other: Pos | tuple):
        return self.__class__(self.rank + other[0], self.file + other[1])

    def is_valid(self):
        return 0 <= self.rank < BOARD_SIZE and 0 <= self.file < BOARD_SIZE 
    



class PieceType(Enum):
    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5

class Colour(Enum):
    WHITE = 0
    BLACK = 1

@dataclass
class Piece:
    piece_type: PieceType
    colour: Colour
    _num_moves: int = 0
    _is_enpassantable: bool = False

    def __str__(self):
        if self.colour == Colour.WHITE:
            return chr(0x2654 + self.piece_type.value)
        else:
            return chr(0x265a + self.piece_type.value)


class Board:
    """Wrapper over a list of lists to ensure they remain a fixed length"""
    def __init__(self, size=8):
        rank0 = [
                Piece(PieceType.ROOK, Colour.WHITE), 
                Piece(PieceType.KNIGHT, Colour.WHITE), 
                Piece(PieceType.BISHOP, Colour.WHITE), 
                Piece(PieceType.QUEEN, Colour.WHITE), 
                Piece(PieceType.KING, Colour.WHITE), 
                Piece(PieceType.BISHOP, Colour.WHITE), 
                Piece(PieceType.KNIGHT, Colour.WHITE), 
                Piece(PieceType.ROOK, Colour.WHITE),
        ]

        rank1 = [Piece(PieceType.PAWN, Colour.WHITE)] * 8

        rank6 = [Piece(PieceType.PAWN, Colour.BLACK)] * 8

        rank7 = [
                Piece(PieceType.ROOK, Colour.BLACK), 
                Piece(PieceType.KNIGHT, Colour.BLACK), 
                Piece(PieceType.BISHOP, Colour.BLACK), 
                Piece(PieceType.QUEEN, Colour.BLACK), 
                Piece(PieceType.KING, Colour.BLACK), 
                Piece(PieceType.BISHOP, Colour.BLACK), 
                Piece(PieceType.KNIGHT, Colour.BLACK), 
                Piece(PieceType.ROOK, Colour.BLACK),
        ]
        
        self._data = []
        for rank in range(size):
            if rank == 0:
                self._data.append(rank0)
            elif rank == 1:
                self._data.append(rank1)
            elif rank == 6:
                self._data.append(rank6)
            elif rank == 7:
                self._data.append(rank7)
            else:
                self._data.append([None] * 8)


        self.size = size

    def __repr__(self) -> str:
        return repr(self._data)
    
    def __str__(self) -> str:
        out = "----"*8 + "-\n"
        for rank in self._data:
            out += "| "
            for piece in rank:
                out += str(piece or " ") + " | "
            out += "\n" + "----"*8 + "-\n"

        return out
    
    def get_piece(self, pos: Pos) -> Piece | None:
        return self._data[pos.rank][pos.file]
    
    def knight_moves(self, pos: Pos) -> list[Pos]:
        piece = self.get_piece(pos)

        if piece is None:
            return []
        if piece.piece_type != PieceType.KNIGHT:
            return []
        
        offsets = (
            (2, 1), (2, -1),
            (1, 2), (-1, 2),
            (-2, 1), (-2, -1),
            (1, -2), (-1, -2)
        )
        valid_moves = []
        for offset in offsets:
            new_pos = pos + offset
            if not new_pos.is_valid():
                continue

            target_piece = self.get_piece(new_pos)
            if target_piece is not None:
                if target_piece.colour != piece.colour:
                    valid_moves.append(new_pos)
            else:
                valid_moves.append(new_pos)

        return valid_moves
    
    def _check_next_space(self, original_piece: Piece, pos: Pos, direction: tuple[int, int]) -> list[Pos]:
        """Recursive function which looks at spaces in turn until the piece can move no further"""
        next_pos = pos + direction
        if not next_pos.is_valid():
            return []
        next_piece = self.get_piece(next_pos)
        if next_piece is None:
            return [next_pos] + self._check_next_space(original_piece, next_pos, direction)
        if next_piece.colour != original_piece.colour:
            return [next_pos]
        return []

    def rook_moves(self, pos: Pos) -> list[Pos]:
        piece = self.get_piece(pos)

        if piece is None:
            return []
        if piece.piece_type != PieceType.ROOK:
            return []
        
        orthoganols = (
            (1, 0), (-1, 0),
            (0, 1), (0, -1)
        )

        valid_moves = []
        for direction in orthoganols:
            valid_moves.extend(self._check_next_space(piece, pos, direction))

        return valid_moves
    
    def bishop_moves(self, pos: Pos) -> list[Pos]:
        piece = self.get_piece(pos)

        if piece is None:
            return []
        if piece.piece_type != PieceType.BISHOP:
            return []
        
        diagonals = (
            (1, 1), (1, -1),
            (-1, 1), (-1, -1)
        )

        valid_moves = []
        for direction in diagonals:
            valid_moves.extend(self._check_next_space(piece, pos, direction))

        return valid_moves
    
    def queen_moves(self, pos: Pos) -> list[Pos]:
        piece = self.get_piece(pos)

        if piece is None:
            return []
        if piece.piece_type != PieceType.QUEEN:
            return []
        
        directions = (
            (1, 0), (-1, 0),
            (0, 1), (0, -1),
            (1, 1), (1, -1),
            (-1, 1), (-1, -1)
        )

        valid_moves = []
        for direction in directions:
            valid_moves.extend(self._check_next_space(piece, pos, direction))

        return valid_moves
    
    def king_moves(self, pos: Pos) -> list[Pos]:
        """
        TODO: Castling
        Does not check for check!
        """
        piece = self.get_piece(pos)

        if piece is None:
            return []
        if piece.piece_type != PieceType.KING:
            return []
        
        directions = (
            (1, 0), (-1, 0),
            (0, 1), (0, -1),
            (1, 1), (1, -1),
            (-1, 1), (-1, -1)
        )

        valid_moves = []
        for direction in directions:
            new_pos = pos + direction
            if not new_pos.is_valid():
                continue

            new_piece = self.get_piece(new_pos)
            if new_piece is None:
                valid_moves.append(new_pos)
            elif new_piece.colour != piece.colour:
                valid_moves.append(new_pos)

        return valid_moves


             
        




class Game:
    pass

b = Board()
print(b)
print(b.king_moves(Pos(0, 4)))