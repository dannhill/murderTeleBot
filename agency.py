class agency:
  # Static variable
  __members: list[str]

  def __init__(self) -> None:
    self.members = []

  def get_members_count(self) -> int:
    return len(self.members)

  def clear(self) -> None:
    self.members.clear()

  def get_members_list(self) -> list[str]:
    return self.members

  def append_member(self, member: str) -> None:
    self.members.append(member)
