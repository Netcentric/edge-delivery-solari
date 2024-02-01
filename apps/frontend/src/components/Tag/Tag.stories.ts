import type { Meta, StoryObj } from '@storybook/react';
import { action } from '@storybook/addon-actions';
import { Tag } from './Tag';

const meta = {
  title: 'Tag',
  component: Tag,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
} satisfies Meta<typeof Tag>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    label: 'intersteller collaboration',
    isSelected: false
  },
};

export const Selected: Story = {
  args: {
    label: 'scientific research',
    isSelected: true,
    onClick: action('on-click'),
  },
};
