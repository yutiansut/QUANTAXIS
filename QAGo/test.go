package main

import (
	"context"
	"testing"

	"github.com/mongodb/mongo-go-driver/bson"
	"github.com/mongodb/mongo-go-driver/mongo"
	"github.com/stretchr/testify/require"
)

func requireCursorLength(t *testing.T, cursor mongo.Cursor, length int) {
	i := 0
	for cursor.Next(context.Background()) {
		i++
	}

	require.NoError(t, cursor.Err())
	require.Equal(t, i, length)
}

func stringSliceEquals(s1 []string, s2 []string) bool {
	if len(s1) != len(s2) {
		return false
	}

	for i := range s1 {
		if s1[i] != s2[i] {
			return false
		}
	}

	return true
}

func containsKey(keys bson.Keys, key string, prefix []string) bool {
	for _, k := range keys {
		if k.Name == key && stringSliceEquals(k.Prefix, prefix) {
			return true
		}
	}

	return false
}

func InsertExamples(t *testing.T, db *mongo.Database) {
	_, err := db.RunCommand(
		context.Background(),
		bson.NewDocument(bson.EC.Int32("dropDatabase", 1)),
	)
	require.NoError(t, err)

	coll := db.Collection("inventory")

	{
		// Start Example 1

		result, err := coll.InsertOne(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("item", "canvas"),
				bson.EC.Int32("qty", 100),
				bson.EC.ArrayFromElements("tags",
					bson.VC.String("cotton"),
				),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 28),
					bson.EC.Double("w", 35.5),
					bson.EC.String("uom", "cm"),
				),
			))

		// End Example 1

		require.NoError(t, err)
		require.NotNil(t, result.InsertedID)
	}

	{
		// Start Example 2

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(bson.EC.String("item", "canvas")),
		)

		// End Example 2

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)

	}

	{
		// Start Example 3

		result, err := coll.InsertMany(
			context.Background(),
			[]interface{}{
				bson.NewDocument(
					bson.EC.String("item", "journal"),
					bson.EC.Int32("qty", 25),
					bson.EC.ArrayFromElements("tags",
						bson.VC.String("blank"),
						bson.VC.String("red"),
					),
					bson.EC.SubDocumentFromElements("size",
						bson.EC.Int32("h", 14),
						bson.EC.Int32("w", 21),
						bson.EC.String("uom", "cm"),
					),
				),
				bson.NewDocument(
					bson.EC.String("item", "mat"),
					bson.EC.Int32("qty", 25),
					bson.EC.ArrayFromElements("tags",
						bson.VC.String("gray"),
					),
					bson.EC.SubDocumentFromElements("size",
						bson.EC.Double("h", 27.9),
						bson.EC.Double("w", 35.5),
						bson.EC.String("uom", "cm"),
					),
				),
				bson.NewDocument(
					bson.EC.String("item", "mousepad"),
					bson.EC.Int32("qty", 25),
					bson.EC.ArrayFromElements("tags",
						bson.VC.String("gel"),
						bson.VC.String("blue"),
					),
					bson.EC.SubDocumentFromElements("size",
						bson.EC.Int32("h", 19),
						bson.EC.Double("w", 22.85),
						bson.EC.String("uom", "cm"),
					),
				),
			})

		// End Example 3

		require.NoError(t, err)
		require.Len(t, result.InsertedIDs, 3)
	}
}

func QueryToplevelFieldsExamples(t *testing.T, db *mongo.Database) {
	_, err := db.RunCommand(
		context.Background(),
		bson.NewDocument(bson.EC.Int32("dropDatabase", 1)),
	)
	require.NoError(t, err)

	coll := db.Collection("inventory")

	{
		// Start Example 6

		docs := []interface{}{
			bson.NewDocument(
				bson.EC.String("item", "journal"),
				bson.EC.Int32("qty", 25),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 14),
					bson.EC.Int32("w", 21),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
			bson.NewDocument(
				bson.EC.String("item", "notebook"),
				bson.EC.Int32("qty", 50),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 8.5),
					bson.EC.Int32("w", 11),
					bson.EC.String("uom", "in"),
				),
				bson.EC.String("status", "A"),
			),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
				bson.EC.Int32("qty", 100),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 8.5),
					bson.EC.Int32("w", 11),
					bson.EC.String("uom", "in"),
				),
				bson.EC.String("status", "D"),
			),
			bson.NewDocument(
				bson.EC.String("item", "planner"),
				bson.EC.Int32("qty", 75),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 22.85),
					bson.EC.Int32("w", 30),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "D"),
			),
			bson.NewDocument(
				bson.EC.String("item", "postcard"),
				bson.EC.Int32("qty", 45),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 10),
					bson.EC.Double("w", 15.25),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
		}

		result, err := coll.InsertMany(context.Background(), docs)

		// End Example 6

		require.NoError(t, err)
		require.Len(t, result.InsertedIDs, 5)
	}

	{
		// Start Example 7

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(),
		)

		// End Example 7

		require.NoError(t, err)
		requireCursorLength(t, cursor, 5)
	}

	{
		// Start Example 9

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(bson.EC.String("status", "D")),
		)

		// End Example 9

		require.NoError(t, err)
		requireCursorLength(t, cursor, 2)
	}

	{
		// Start Example 10

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("status",
					bson.EC.ArrayFromElements("$in",
						bson.VC.String("A"),
						bson.VC.String("D"),
					),
				),
			))

		// End Example 10

		require.NoError(t, err)
		requireCursorLength(t, cursor, 5)
	}

	{
		// Start Example 11

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
				bson.EC.SubDocumentFromElements("qty",
					bson.EC.Int32("$lt", 30),
				),
			))

		// End Example 11

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

	{
		// Start Example 12

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.ArrayFromElements("$or",
					bson.VC.DocumentFromElements(
						bson.EC.String("status", "A"),
					),
					bson.VC.DocumentFromElements(
						bson.EC.SubDocumentFromElements("qty",
							bson.EC.Int32("$lt", 30),
						),
					),
				),
			))

		// End Example 12

		require.NoError(t, err)
		requireCursorLength(t, cursor, 3)
	}

	{
		// Start Example 13

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
				bson.EC.ArrayFromElements("$or",
					bson.VC.DocumentFromElements(
						bson.EC.SubDocumentFromElements("qty",
							bson.EC.Int32("$lt", 30),
						),
					),
					bson.VC.DocumentFromElements(
						bson.EC.Regex("item", "^p", ""),
					),
				),
			))

		// End Example 13

		require.NoError(t, err)
		requireCursorLength(t, cursor, 2)
	}

}

func QueryEmbeddedDocumentsExamples(t *testing.T, db *mongo.Database) {
	_, err := db.RunCommand(
		context.Background(),
		bson.NewDocument(bson.EC.Int32("dropDatabase", 1)),
	)
	require.NoError(t, err)

	coll := db.Collection("inventory")

	{
		// Start Example 14

		docs := []interface{}{
			bson.NewDocument(
				bson.EC.String("item", "journal"),
				bson.EC.Int32("qty", 25),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 14),
					bson.EC.Int32("w", 21),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
			bson.NewDocument(
				bson.EC.String("item", "notebook"),
				bson.EC.Int32("qty", 50),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 8.5),
					bson.EC.Int32("w", 11),
					bson.EC.String("uom", "in"),
				),
				bson.EC.String("status", "A"),
			),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
				bson.EC.Int32("qty", 100),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 8.5),
					bson.EC.Int32("w", 11),
					bson.EC.String("uom", "in"),
				),
				bson.EC.String("status", "D"),
			),
			bson.NewDocument(
				bson.EC.String("item", "planner"),
				bson.EC.Int32("qty", 75),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 22.85),
					bson.EC.Int32("w", 30),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "D"),
			),
			bson.NewDocument(
				bson.EC.String("item", "postcard"),
				bson.EC.Int32("qty", 45),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 10),
					bson.EC.Double("w", 15.25),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
		}

		result, err := coll.InsertMany(context.Background(), docs)

		// End Example 14

		require.NoError(t, err)
		require.Len(t, result.InsertedIDs, 5)
	}

	{
		// Start Example 15

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 14),
					bson.EC.Int32("w", 21),
					bson.EC.String("uom", "cm"),
				),
			))

		// End Example 15

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

	{
		// Start Example 16

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("w", 21),
					bson.EC.Int32("h", 14),
					bson.EC.String("uom", "cm"),
				),
			))

		// End Example 16

		require.NoError(t, err)
		requireCursorLength(t, cursor, 0)
	}

	{
		// Start Example 17

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("size.uom", "in"),
			))

		// End Example 17

		require.NoError(t, err)
		requireCursorLength(t, cursor, 2)
	}

	{
		// Start Example 18

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("size.h",
					bson.EC.Int32("$lt", 15),
				),
			))

		// End Example 18

		require.NoError(t, err)
		requireCursorLength(t, cursor, 4)
	}

	{
		// Start Example 19

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("size.h",
					bson.EC.Int32("$lt", 15),
				),
				bson.EC.String("size.uom", "in"),
				bson.EC.String("status", "D"),
			))

		// End Example 19

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

}

func QueryArraysExamples(t *testing.T, db *mongo.Database) {
	_, err := db.RunCommand(
		context.Background(),
		bson.NewDocument(bson.EC.Int32("dropDatabase", 1)),
	)
	require.NoError(t, err)

	coll := db.Collection("inventory")

	{
		// Start Example 20

		docs := []interface{}{
			bson.NewDocument(
				bson.EC.String("item", "journal"),
				bson.EC.Int32("qty", 25),
				bson.EC.ArrayFromElements("tags",
					bson.VC.String("blank"),
					bson.VC.String("red"),
				),
				bson.EC.ArrayFromElements("dim_cm",
					bson.VC.Int32(14),
					bson.VC.Int32(21),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "notebook"),
				bson.EC.Int32("qty", 50),
				bson.EC.ArrayFromElements("tags",
					bson.VC.String("red"),
					bson.VC.String("blank"),
				),
				bson.EC.ArrayFromElements("dim_cm",
					bson.VC.Int32(14),
					bson.VC.Int32(21),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
				bson.EC.Int32("qty", 100),
				bson.EC.ArrayFromElements("tags",
					bson.VC.String("red"),
					bson.VC.String("blank"),
					bson.VC.String("plain"),
				),
				bson.EC.ArrayFromElements("dim_cm",
					bson.VC.Int32(14),
					bson.VC.Int32(21),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "planner"),
				bson.EC.Int32("qty", 75),
				bson.EC.ArrayFromElements("tags",
					bson.VC.String("blank"),
					bson.VC.String("red"),
				),
				bson.EC.ArrayFromElements("dim_cm",
					bson.VC.Double(22.85),
					bson.VC.Int32(30),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "postcard"),
				bson.EC.Int32("qty", 45),
				bson.EC.ArrayFromElements("tags",
					bson.VC.String("blue"),
				),
				bson.EC.ArrayFromElements("dim_cm",
					bson.VC.Int32(10),
					bson.VC.Double(15.25),
				),
			),
		}

		result, err := coll.InsertMany(context.Background(), docs)

		// End Example 20

		require.NoError(t, err)
		require.Len(t, result.InsertedIDs, 5)
	}

	{
		// Start Example 21

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.ArrayFromElements("tags",
					bson.VC.String("red"),
					bson.VC.String("blank"),
				),
			))

		// End Example 21

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

	{
		// Start Example 22

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("tags",
					bson.EC.ArrayFromElements("$all",
						bson.VC.String("red"),
						bson.VC.String("blank"),
					),
				),
			))

		// End Example 22

		require.NoError(t, err)
		requireCursorLength(t, cursor, 4)
	}

	{
		// Start Example 23

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("tags", "red"),
			))

		// End Example 23

		require.NoError(t, err)
		requireCursorLength(t, cursor, 4)
	}

	{
		// Start Example 24

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("dim_cm",
					bson.EC.Int32("$gt", 25),
				),
			))

		// End Example 24

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

	{
		// Start Example 25

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("dim_cm",
					bson.EC.Int32("$gt", 15),
					bson.EC.Int32("$lt", 20),
				),
			))

		// End Example 25

		require.NoError(t, err)
		requireCursorLength(t, cursor, 4)
	}

	{
		// Start Example 26

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("dim_cm",
					bson.EC.SubDocumentFromElements("$elemMatch",
						bson.EC.Int32("$gt", 22),
						bson.EC.Int32("$lt", 30),
					),
				),
			))

		// End Example 26

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

	{
		// Start Example 27

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("dim_cm.1",
					bson.EC.Int32("$gt", 25),
				),
			))

		// End Example 27

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

	{
		// Start Example 28

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("tags",
					bson.EC.Int32("$size", 3),
				),
			))

		// End Example 28

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

}

func QueryArrayEmbeddedDocumentsExamples(t *testing.T, db *mongo.Database) {
	_, err := db.RunCommand(
		context.Background(),
		bson.NewDocument(bson.EC.Int32("dropDatabase", 1)),
	)
	require.NoError(t, err)

	coll := db.Collection("inventory")

	{
		// Start Example 29

		docs := []interface{}{
			bson.NewDocument(
				bson.EC.String("item", "journal"),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "A"),
						bson.EC.Int32("qty", 5),
					),
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "C"),
						bson.EC.Int32("qty", 15),
					),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "notebook"),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "C"),
						bson.EC.Int32("qty", 5),
					),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "A"),
						bson.EC.Int32("qty", 60),
					),
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "B"),
						bson.EC.Int32("qty", 15),
					),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "planner"),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "A"),
						bson.EC.Int32("qty", 40),
					),
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "B"),
						bson.EC.Int32("qty", 5),
					),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "postcard"),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "B"),
						bson.EC.Int32("qty", 15),
					),
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "C"),
						bson.EC.Int32("qty", 35),
					),
				),
			),
		}

		result, err := coll.InsertMany(context.Background(), docs)

		// End Example 29

		require.NoError(t, err)
		require.Len(t, result.InsertedIDs, 5)
	}

	{
		// Start Example 30

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("instock",
					bson.EC.String("warehouse", "A"),
					bson.EC.Int32("qty", 5),
				),
			))

		// End Example 30

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

	{
		// Start Example 31

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("instock",
					bson.EC.Int32("qty", 5),
					bson.EC.String("warehouse", "A"),
				),
			))

		// End Example 31

		require.NoError(t, err)
		requireCursorLength(t, cursor, 0)
	}

	{
		// Start Example 32

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("instock.0.qty",
					bson.EC.Int32("$lte", 20),
				),
			))

		// End Example 32

		require.NoError(t, err)
		requireCursorLength(t, cursor, 3)
	}

	{
		// Start Example 33

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("instock.qty",
					bson.EC.Int32("$lte", 20),
				),
			))

		// End Example 33

		require.NoError(t, err)
		requireCursorLength(t, cursor, 5)
	}

	{
		// Start Example 34

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("instock",
					bson.EC.SubDocumentFromElements("$elemMatch",
						bson.EC.Int32("qty", 5),
						bson.EC.String("warehouse", "A"),
					),
				),
			))

		// End Example 34

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

	{
		// Start Example 35

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("instock",
					bson.EC.SubDocumentFromElements("$elemMatch",
						bson.EC.SubDocumentFromElements("qty",
							bson.EC.Int32("$gt", 10),
							bson.EC.Int32("$lte", 20),
						),
					),
				),
			))

		// End Example 35

		require.NoError(t, err)
		requireCursorLength(t, cursor, 3)
	}

	{
		// Start Example 36

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("instock.qty",
					bson.EC.Int32("$gt", 10),
					bson.EC.Int32("$lte", 20),
				),
			))

		// End Example 36

		require.NoError(t, err)
		requireCursorLength(t, cursor, 4)
	}

	{
		// Start Example 37

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.Int32("instock.qty", 5),
				bson.EC.String("instock.warehouse", "A"),
			))

		// End Example 37

		require.NoError(t, err)
		requireCursorLength(t, cursor, 2)
	}
}

func QueryNullMissingFieldsExamples(t *testing.T, db *mongo.Database) {
	_, err := db.RunCommand(
		context.Background(),
		bson.NewDocument(bson.EC.Int32("dropDatabase", 1)),
	)
	require.NoError(t, err)

	coll := db.Collection("inventory")

	{
		// Start Example 38

		docs := []interface{}{
			bson.NewDocument(
				bson.EC.Int32("_id", 1),
				bson.EC.Null("item"),
			),
			bson.NewDocument(
				bson.EC.Int32("_id", 2),
			),
		}

		result, err := coll.InsertMany(context.Background(), docs)

		// End Example 38

		require.NoError(t, err)
		require.Len(t, result.InsertedIDs, 2)
	}

	{
		// Start Example 39

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.Null("item"),
			))

		// End Example 39

		require.NoError(t, err)
		requireCursorLength(t, cursor, 2)
	}

	{
		// Start Example 40

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("item",
					bson.EC.Int32("$type", 10),
				),
			))

		// End Example 40

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}

	{
		// Start Example 41

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("item",
					bson.EC.Boolean("$exists", false),
				),
			))

		// End Example 41

		require.NoError(t, err)
		requireCursorLength(t, cursor, 1)
	}
}

func ProjectionExamples(t *testing.T, db *mongo.Database) {
	_, err := db.RunCommand(
		context.Background(),
		bson.NewDocument(bson.EC.Int32("dropDatabase", 1)),
	)
	require.NoError(t, err)

	coll := db.Collection("inventory")

	{
		// Start Example 42

		docs := []interface{}{
			bson.NewDocument(
				bson.EC.String("item", "journal"),
				bson.EC.String("status", "A"),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 14),
					bson.EC.Int32("w", 21),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "A"),
						bson.EC.Int32("qty", 5),
					),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "notebook"),
				bson.EC.String("status", "A"),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 8.5),
					bson.EC.Double("w", 11),
					bson.EC.String("uom", "in"),
				),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "EC"),
						bson.EC.Int32("qty", 5),
					),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
				bson.EC.String("status", "D"),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 8.5),
					bson.EC.Double("w", 11),
					bson.EC.String("uom", "in"),
				),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "A"),
						bson.EC.Int32("qty", 60),
					),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "planner"),
				bson.EC.String("status", "D"),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 22.85),
					bson.EC.Int32("w", 30),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "A"),
						bson.EC.Int32("qty", 40),
					),
				),
			),
			bson.NewDocument(
				bson.EC.String("item", "postcard"),
				bson.EC.String("status", "A"),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 10),
					bson.EC.Double("w", 15.25),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "B"),
						bson.EC.Int32("qty", 15),
					),
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "EC"),
						bson.EC.Int32("qty", 35),
					),
				),
			),
		}

		result, err := coll.InsertMany(context.Background(), docs)

		// End Example 42

		require.NoError(t, err)
		require.Len(t, result.InsertedIDs, 5)
	}

	{
		// Start Example 43

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
			))

		// End Example 43

		require.NoError(t, err)
		requireCursorLength(t, cursor, 3)
	}

	{
		// Start Example 44

		projection, err := mongo.Opt.Projection(bson.NewDocument(
			bson.EC.Int32("item", 1),
			bson.EC.Int32("status", 1),
		))
		require.NoError(t, err)

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
			),
			projection,
		)

		// End Example 44

		require.NoError(t, err)

		doc := bson.NewDocument()
		for cursor.Next(context.Background()) {
			err := cursor.Decode(doc)
			require.NoError(t, err)

			keys, err := doc.Keys(false)
			require.NoError(t, err)

			require.True(t, containsKey(keys, "_id", nil))
			require.True(t, containsKey(keys, "item", nil))
			require.True(t, containsKey(keys, "status", nil))
			require.False(t, containsKey(keys, "size", nil))
			require.False(t, containsKey(keys, "instock", nil))
		}

		require.NoError(t, cursor.Err())
	}

	{
		// Start Example 45

		projection, err := mongo.Opt.Projection(bson.NewDocument(
			bson.EC.Int32("item", 1),
			bson.EC.Int32("status", 1),
			bson.EC.Int32("_id", 0),
		))
		require.NoError(t, err)

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
			),
			projection,
		)

		// End Example 45

		require.NoError(t, err)

		doc := bson.NewDocument()
		for cursor.Next(context.Background()) {
			err := cursor.Decode(doc)
			require.NoError(t, err)

			keys, err := doc.Keys(false)
			require.NoError(t, err)

			require.False(t, containsKey(keys, "_id", nil))
			require.True(t, containsKey(keys, "item", nil))
			require.True(t, containsKey(keys, "status", nil))
			require.False(t, containsKey(keys, "size", nil))
			require.False(t, containsKey(keys, "instock", nil))
		}

		require.NoError(t, cursor.Err())
	}

	{
		// Start Example 46

		projection, err := mongo.Opt.Projection(bson.NewDocument(
			bson.EC.Int32("status", 0),
			bson.EC.Int32("instock", 0),
		))
		require.NoError(t, err)

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
			),
			projection,
		)

		// End Example 46

		require.NoError(t, err)

		doc := bson.NewDocument()
		for cursor.Next(context.Background()) {
			err := cursor.Decode(doc)
			require.NoError(t, err)

			keys, err := doc.Keys(false)
			require.NoError(t, err)

			require.True(t, containsKey(keys, "_id", nil))
			require.True(t, containsKey(keys, "item", nil))
			require.False(t, containsKey(keys, "status", nil))
			require.True(t, containsKey(keys, "size", nil))
			require.False(t, containsKey(keys, "instock", nil))
		}

		require.NoError(t, cursor.Err())
	}

	{
		// Start Example 47

		projection, err := mongo.Opt.Projection(bson.NewDocument(
			bson.EC.Int32("item", 1),
			bson.EC.Int32("status", 1),
			bson.EC.Int32("size.uom", 1),
		))
		require.NoError(t, err)

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
			),
			projection,
		)

		// End Example 47

		require.NoError(t, err)

		doc := bson.NewDocument()
		for cursor.Next(context.Background()) {
			err := cursor.Decode(doc)
			require.NoError(t, err)

			keys, err := doc.Keys(true)
			require.NoError(t, err)

			require.True(t, containsKey(keys, "_id", nil))
			require.True(t, containsKey(keys, "item", nil))
			require.True(t, containsKey(keys, "status", nil))
			require.True(t, containsKey(keys, "size", nil))
			require.False(t, containsKey(keys, "instock", nil))

			require.True(t, containsKey(keys, "uom", []string{"size"}))
			require.False(t, containsKey(keys, "h", []string{"size"}))
			require.False(t, containsKey(keys, "w", []string{"size"}))

		}

		require.NoError(t, cursor.Err())
	}

	{
		// Start Example 48

		projection, err := mongo.Opt.Projection(bson.NewDocument(
			bson.EC.Int32("size.uom", 0),
		))
		require.NoError(t, err)

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
			),
			projection,
		)

		// End Example 48

		require.NoError(t, err)

		doc := bson.NewDocument()
		for cursor.Next(context.Background()) {
			err := cursor.Decode(doc)
			require.NoError(t, err)

			keys, err := doc.Keys(true)
			require.NoError(t, err)

			require.True(t, containsKey(keys, "_id", nil))
			require.True(t, containsKey(keys, "item", nil))
			require.True(t, containsKey(keys, "status", nil))
			require.True(t, containsKey(keys, "size", nil))
			require.True(t, containsKey(keys, "instock", nil))

			require.False(t, containsKey(keys, "uom", []string{"size"}))
			require.True(t, containsKey(keys, "h", []string{"size"}))
			require.True(t, containsKey(keys, "w", []string{"size"}))

		}

		require.NoError(t, cursor.Err())
	}

	{
		// Start Example 49

		projection, err := mongo.Opt.Projection(bson.NewDocument(
			bson.EC.Int32("item", 1),
			bson.EC.Int32("status", 1),
			bson.EC.Int32("instock.qty", 1),
		))
		require.NoError(t, err)

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
			),
			projection,
		)

		// End Example 49

		require.NoError(t, err)

		doc := bson.NewDocument()
		for cursor.Next(context.Background()) {
			err := cursor.Decode(doc)
			require.NoError(t, err)

			keys, err := doc.Keys(true)
			require.NoError(t, err)

			require.True(t, containsKey(keys, "_id", nil))
			require.True(t, containsKey(keys, "item", nil))
			require.True(t, containsKey(keys, "status", nil))
			require.False(t, containsKey(keys, "size", nil))
			require.True(t, containsKey(keys, "instock", nil))

			instock, err := doc.Lookup("instock")
			require.NoError(t, err)

			arr := instock.Value().MutableArray()

			for i := uint(0); i < uint(arr.Len()); i++ {
				elem, err := arr.Lookup(i)
				require.NoError(t, err)

				require.Equal(t, bson.TypeEmbeddedDocument, elem.Type())
				subdoc := elem.MutableDocument()

				require.Equal(t, 1, subdoc.Len())
				_, err = subdoc.Lookup("qty")
				require.NoError(t, err)
			}
		}

		require.NoError(t, cursor.Err())
	}

	{
		// Start Example 50

		projection, err := mongo.Opt.Projection(bson.NewDocument(
			bson.EC.Int32("item", 1),
			bson.EC.Int32("status", 1),
			bson.EC.SubDocumentFromElements("instock",
				bson.EC.Int32("$slice", -1),
			),
		))
		require.NoError(t, err)

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
			),
			projection,
		)

		// End Example 50

		require.NoError(t, err)

		doc := bson.NewDocument()
		for cursor.Next(context.Background()) {
			err := cursor.Decode(doc)
			require.NoError(t, err)

			keys, err := doc.Keys(true)
			require.NoError(t, err)

			require.True(t, containsKey(keys, "_id", nil))
			require.True(t, containsKey(keys, "item", nil))
			require.True(t, containsKey(keys, "status", nil))
			require.False(t, containsKey(keys, "size", nil))
			require.True(t, containsKey(keys, "instock", nil))

			instock, err := doc.Lookup("instock")
			require.NoError(t, err)
			require.Equal(t, instock.Value().MutableArray().Len(), 1)
		}

		require.NoError(t, cursor.Err())
	}
}

func UpdateExamples(t *testing.T, db *mongo.Database) {
	_, err := db.RunCommand(
		context.Background(),
		bson.NewDocument(bson.EC.Int32("dropDatabase", 1)),
	)
	require.NoError(t, err)

	coll := db.Collection("inventory")

	{
		// Start Example 51

		docs := []interface{}{
			bson.NewDocument(
				bson.EC.String("item", "canvas"),
				bson.EC.Int32("qty", 100),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 28),
					bson.EC.Double("w", 35.5),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
			bson.NewDocument(
				bson.EC.String("item", "journal"),
				bson.EC.Int32("qty", 25),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 14),
					bson.EC.Int32("w", 21),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
			bson.NewDocument(
				bson.EC.String("item", "mat"),
				bson.EC.Int32("qty", 85),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 27.9),
					bson.EC.Double("w", 35.5),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
			bson.NewDocument(
				bson.EC.String("item", "mousepad"),
				bson.EC.Int32("qty", 25),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 19),
					bson.EC.Double("w", 22.85),
					bson.EC.String("uom", "in"),
				),
				bson.EC.String("status", "P"),
			),
			bson.NewDocument(
				bson.EC.String("item", "notebook"),
				bson.EC.Int32("qty", 50),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 8.5),
					bson.EC.Int32("w", 11),
					bson.EC.String("uom", "in"),
				),
				bson.EC.String("status", "P"),
			),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
				bson.EC.Int32("qty", 100),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 8.5),
					bson.EC.Int32("w", 11),
					bson.EC.String("uom", "in"),
				),
				bson.EC.String("status", "D"),
			),
			bson.NewDocument(
				bson.EC.String("item", "planner"),
				bson.EC.Int32("qty", 75),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 22.85),
					bson.EC.Int32("w", 30),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "D"),
			),
			bson.NewDocument(
				bson.EC.String("item", "postcard"),
				bson.EC.Int32("qty", 45),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 10),
					bson.EC.Double("w", 15.25),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
			bson.NewDocument(
				bson.EC.String("item", "sketchbook"),
				bson.EC.Int32("qty", 80),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 14),
					bson.EC.Int32("w", 21),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
			bson.NewDocument(
				bson.EC.String("item", "sketch pad"),
				bson.EC.Int32("qty", 95),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 22.85),
					bson.EC.Double("w", 30.5),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
		}

		result, err := coll.InsertMany(context.Background(), docs)

		// End Example 51

		require.NoError(t, err)
		require.Len(t, result.InsertedIDs, 10)
	}

	{
		// Start Example 52

		result, err := coll.UpdateOne(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
			),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("$set",
					bson.EC.String("size.uom", "cm"),
					bson.EC.String("status", "P"),
				),
				bson.EC.SubDocumentFromElements("$currentDate",
					bson.EC.Boolean("lastModified", true),
				),
			),
		)

		// End Example 52

		require.NoError(t, err)
		require.Equal(t, int64(1), result.MatchedCount)
		require.Equal(t, int64(1), result.ModifiedCount)

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
			))

		require.NoError(t, err)

		doc := bson.NewDocument()
		for cursor.Next(context.Background()) {
			err := cursor.Decode(doc)
			require.NoError(t, err)

			uom, err := doc.Lookup("size", "uom")
			require.NoError(t, err)
			require.Equal(t, uom.Value().StringValue(), "cm")

			status, err := doc.Lookup("status")
			require.NoError(t, err)
			require.Equal(t, status.Value().StringValue(), "P")

			keys, err := doc.Keys(false)
			require.NoError(t, err)
			require.True(t, containsKey(keys, "lastModified", nil))
		}

		require.NoError(t, cursor.Err())
	}

	{
		// Start Example 53

		result, err := coll.UpdateMany(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("qty",
					bson.EC.Int32("$lt", 50),
				),
			),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("$set",
					bson.EC.String("size.uom", "cm"),
					bson.EC.String("status", "P"),
				),
				bson.EC.SubDocumentFromElements("$currentDate",
					bson.EC.Boolean("lastModified", true),
				),
			),
		)

		// End Example 53

		require.NoError(t, err)
		require.Equal(t, int64(3), result.MatchedCount)
		require.Equal(t, int64(3), result.ModifiedCount)

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.SubDocumentFromElements("qty",
					bson.EC.Int32("$lt", 50),
				),
			))

		require.NoError(t, err)

		doc := bson.NewDocument()
		for cursor.Next(context.Background()) {
			err := cursor.Decode(doc)
			require.NoError(t, err)

			uom, err := doc.Lookup("size", "uom")
			require.NoError(t, err)
			require.Equal(t, uom.Value().StringValue(), "cm")

			status, err := doc.Lookup("status")
			require.NoError(t, err)
			require.Equal(t, status.Value().StringValue(), "P")

			keys, err := doc.Keys(false)
			require.NoError(t, err)
			require.True(t, containsKey(keys, "lastModified", nil))
		}

		require.NoError(t, cursor.Err())
	}

	{
		// Start Example 54

		result, err := coll.ReplaceOne(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
			),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
				bson.EC.ArrayFromElements("instock",
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "A"),
						bson.EC.Int32("qty", 60),
					),
					bson.VC.DocumentFromElements(
						bson.EC.String("warehouse", "B"),
						bson.EC.Int32("qty", 40),
					),
				),
			),
		)

		// End Example 54

		require.NoError(t, err)
		require.Equal(t, int64(1), result.MatchedCount)
		require.Equal(t, int64(1), result.ModifiedCount)

		cursor, err := coll.Find(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
			))

		require.NoError(t, err)

		doc := bson.NewDocument()
		for cursor.Next(context.Background()) {
			err := cursor.Decode(doc)
			require.NoError(t, err)

			keys, err := doc.Keys(false)
			require.NoError(t, err)
			require.Len(t, keys, 3)

			require.True(t, containsKey(keys, "_id", nil))
			require.True(t, containsKey(keys, "item", nil))
			require.True(t, containsKey(keys, "instock", nil))

			instock, err := doc.Lookup("instock")
			require.NoError(t, err)
			require.Equal(t, instock.Value().MutableArray().Len(), 2)

		}

		require.NoError(t, cursor.Err())
	}

}

func DeleteExamples(t *testing.T, db *mongo.Database) {
	_, err := db.RunCommand(
		context.Background(),
		bson.NewDocument(bson.EC.Int32("dropDatabase", 1)),
	)
	require.NoError(t, err)

	coll := db.Collection("inventory")

	{
		// Start Example 55
		docs := []interface{}{
			bson.NewDocument(
				bson.EC.String("item", "journal"),
				bson.EC.Int32("qty", 25),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 14),
					bson.EC.Int32("w", 21),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
			bson.NewDocument(
				bson.EC.String("item", "notebook"),
				bson.EC.Int32("qty", 50),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 8.5),
					bson.EC.Int32("w", 11),
					bson.EC.String("uom", "in"),
				),
				bson.EC.String("status", "P"),
			),
			bson.NewDocument(
				bson.EC.String("item", "paper"),
				bson.EC.Int32("qty", 100),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 8.5),
					bson.EC.Int32("w", 11),
					bson.EC.String("uom", "in"),
				),
				bson.EC.String("status", "D"),
			),
			bson.NewDocument(
				bson.EC.String("item", "planner"),
				bson.EC.Int32("qty", 75),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Double("h", 22.85),
					bson.EC.Int32("w", 30),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "D"),
			),
			bson.NewDocument(
				bson.EC.String("item", "postcard"),
				bson.EC.Int32("qty", 45),
				bson.EC.SubDocumentFromElements("size",
					bson.EC.Int32("h", 10),
					bson.EC.Double("w", 15.25),
					bson.EC.String("uom", "cm"),
				),
				bson.EC.String("status", "A"),
			),
		}

		result, err := coll.InsertMany(context.Background(), docs)

		// End Example 55

		require.NoError(t, err)
		require.Len(t, result.InsertedIDs, 5)
	}

	{
		// Start Example 57

		result, err := coll.DeleteMany(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "A"),
			),
		)

		// End Example 57

		require.NoError(t, err)
		require.Equal(t, int64(2), result.DeletedCount)
	}

	{
		// Start Example 58

		result, err := coll.DeleteOne(
			context.Background(),
			bson.NewDocument(
				bson.EC.String("status", "D"),
			),
		)

		// End Example 58

		require.NoError(t, err)
		require.Equal(t, int64(1), result.DeletedCount)

	}

	{
		// Start Example 56

		result, err := coll.DeleteMany(context.Background(), bson.NewDocument())

		// End Example 56

		require.NoError(t, err)
		require.Equal(t, int64(2), result.DeletedCount)
	}
}