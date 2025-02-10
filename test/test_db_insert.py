from app.models import OperationsStats
from app.database import SessionLocal

def test_insert_stats():
    db = SessionLocal()  
    try:
        # Insère une nouvelle entrée dans la table operations_stats
        new_stat = OperationsStats(operation_id='INFO', count=5)
        db.add(new_stat)
        db.commit()  
        db.refresh(new_stat) 
        print(f"Stat inserted with ID: {new_stat.operation_id} and Count: {new_stat.count}")
    except Exception as e:
        print(f"Error inserting stats: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    test_insert_stats()
