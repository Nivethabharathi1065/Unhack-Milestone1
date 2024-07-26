import pandas as pd

# Load Care Areas data
care_areas = pd.read_csv('CareAreas.csv', header=None)
care_areas.columns = ['id', 'x1', 'x2', 'y1', 'y2']

# Load Metadata
metadata = pd.read_csv('metadata.csv')
main_field_size = int(metadata['Main Field Size'].iloc[0])
sub_field_size = int(metadata['Sub Field size'].iloc[0])


def generate_main_fields_from_care_areas(care_areas, main_field_size):
    main_fields = []
    for _, row in care_areas.iterrows():
        x1, x2, y1, y2 = int(row['x1']), int(row['x2']), int(row['y1']), int(row['y2'])
        main_fields.append([x1, x1 + main_field_size, y1, y1 + main_field_size])
    return pd.DataFrame(main_fields, columns=['x1', 'x2', 'y1', 'y2'])


main_fields_minimal = generate_main_fields_from_care_areas(care_areas, main_field_size)


def generate_sub_fields_from_care_areas(care_areas, sub_field_size):
    sub_fields = []
    for _, row in care_areas.iterrows():
        x1, x2, y1, y2 = int(row['x1']), int(row['x2']), int(row['y1']), int(row['y2'])

        # Compute subfield ranges using plain Python
        x_range = list(range(x1, x2, sub_field_size))
        y_range = list(range(y1, y2, sub_field_size))

        for x in x_range:
            for y in y_range:
                sub_x2 = min(x + sub_field_size, x2)
                sub_y2 = min(y + sub_field_size, y2)
                sub_fields.append([x, sub_x2, y, sub_y2, row['id']])

    return pd.DataFrame(sub_fields, columns=['x1', 'x2', 'y1', 'y2', 'CareArea ID'])


sub_fields = generate_sub_fields_from_care_areas(care_areas, sub_field_size)

# Save results to CSV
main_fields_minimal.to_csv('MainFieldsOP.csv', index_label='ID', header=False)
sub_fields.to_csv('SubFieldsOP.csv', index_label='ID', header=False)
