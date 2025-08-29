from sqlalchemy import Column,ForeignKey,Integer,String,create_engine

from sqlalchemy.orm import declarative_base,relationship,sessionmaker

db_url="sqlite:///database.db"

engine=create_engine(db_url)
Base=declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class NodeAssociation(Base):
    __tablename__ ="node_associations"
    id = Column(Integer,primary_key=True)
    current_node_id = Column(Integer,ForeignKey("nodes.id"))
    next_node_id = Column(Integer,ForeignKey('nodes.id'))

class Node(Base):
    __tablename__ = "nodes"
    id = Column(Integer,primary_key=True)
    value = Column(Integer,nullable=False)
    next_node = relationship("Node",secondary="node_associations",primaryjoin="NodeAssociation.current_node_id == Node.id",secondaryjoin="NodeAssociation.next_node_id ==Node.id",uselist=False)

    def __repr__(self):
        return f"<Node value={self.value}>"
    
Base.metadata.create_all(engine)

node1 = Node(value=1)
node2 = Node(value=2)
node3 = Node(value=3)

node1.next_node = node2
node2.next_node = node3

session.add_all([node1,node2,node3])
session.commit()

print(node1)
print(node2)
print(node3)
