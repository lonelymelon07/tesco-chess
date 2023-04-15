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

    def __str__(self):
        return "W" if self == Colour.WHITE else "B"

@dataclass
class Piece:
    piece_type: PieceType
    colour: Colour
    _num_moves: int = 0
    _has_just_moved: bool = False
    _is_enpassantable: bool = False
    _can_castle: bool = False

    def __str__(self):
        if self.colour == Colour.WHITE:
            return chr(0x2654 + self.piece_type.value)
        else:
            return chr(0x265a + self.piece_type.value)
    
    @property
    def has_moved(self) -> bool:
        return self._num_moves > 0

class Board:
    """Wrapper over a list of lists to ensure they remain a fixed length"""
    def __init__(self, size=8):
        # I couldn't be arsed to do this in code so manually it is
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
        out = "+----"*8 + "+\n"
        for rank in reversed(self._data):
            out += "| "
            for piece in rank:
                out += f"{piece.colour}{piece} | " if piece is not None else "   | "
            out += "\n" + "+----"*8 + "+\n"

        return out
    
    def _dbg_print_positions(self):
        print([[(i, j) for j in range(self.size)] for i in range(self.size)])
    
    def _is_capturable(self, pos: Pos, captor: Piece) -> bool:
        if not pos.is_valid():
            return False
        
        piece = self.get_piece(pos)
        if piece is None or piece.colour == captor.colour:
            return False
        
        return True

    def get_piece(self, pos: Pos) -> Piece | None:
        return self._data[pos.rank][pos.file]
     
    def _force_move(self, origin: Pos, destination: Pos):
        self._set_piece(destination, self.get_piece(origin))
        self._set_piece(origin, None)
    
    def _set_piece(self, pos: Pos, piece: Piece | None):
        self._data[pos.rank][pos.file] = piece

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
        # somehow this worked first time!
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

    def pawn_moves(self, pos: Pos) -> list[Pos]:
        """
        TODO: en passant
        """
        piece = self.get_piece(pos)

        if piece is None:
            return []
        if piece.piece_type != PieceType.PAWN:
            return []
        
        if piece.colour == Colour.WHITE:
            dir_mult = 1
        else:
            dir_mult = -1

        valid_moves = []

        # first check space in front
        new_pos = pos + (1 * dir_mult, 0)
        if new_pos.is_valid() and self.get_piece(new_pos) is None:
            valid_moves.append(new_pos)

        # if the first move is not valid then jumping two ahead isn't either!
        if valid_moves and not piece.has_moved:
            new_pos = pos + (2 * dir_mult, 0)
            if new_pos.is_valid() and self.get_piece(new_pos) is None:
                valid_moves.append(new_pos)

        # now for sidewaysing!
        for direction in ((1 * dir_mult, 1), (1 * dir_mult, -1)):
            new_pos = pos + direction
            if not new_pos.is_valid() or (victim := self.get_piece(new_pos)) is None:
                continue
            if victim.colour == piece.colour:
                continue
            valid_moves.append(new_pos)

        return valid_moves
    
    def move(self, origin: Pos, destination: Pos) -> bool:
        piece = self.get_piece(origin)
        if piece is None:
            return False
        
        match self.get_piece(origin).piece_type:
            case PieceType.KING:
                valid_moves = self.king_moves(origin)
            case PieceType.QUEEN:
                valid_moves = self.queen_moves(origin)
            case PieceType.ROOK:
                valid_moves = self.rook_moves(origin)
            case PieceType.BISHOP:
                valid_moves = self.bishop_moves(origin)
            case PieceType.KNIGHT:
                valid_moves = self.knight_moves(origin)
            case PieceType.PAWN:
                valid_moves = self.pawn_moves(origin)
        if destination not in valid_moves:
            return False
        
        self._force_move(origin, destination)
        return True
        



class Game:
    pass

### TEMPORARY!!!
board = Board()

while True:
    print(board)

    origin = [int(s.strip()) for s in input("Piece to move: ").split(',')]
    origin = Pos(origin[0], origin[1])
    destination = [int(s.strip()) for s in input("destination: ").split(',')]
    destination = Pos(destination[0], destination[1])

    print(board.move(origin, destination))